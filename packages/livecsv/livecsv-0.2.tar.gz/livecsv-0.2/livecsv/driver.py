from sqlalchemy.engine import default
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.dialects import registry
import time
import duckdb

########################################################################
# 1. The Connection Provider
########################################################################
# This helper class creates (and re‑creates) an in‑memory DuckDB engine,
# loading the CSV into a table. It also implements a caching timeout.
#
# When a DBAPI‑level connection is requested, it returns a raw connection
# from the underlying DuckDB engine.
########################################################################

class LiveCSVConnectionProvider:
    def __init__(self, cache_minutes, tablename, csv_url):
        """
        :param cache_minutes: Cache lifetime in minutes. Zero means unlimited.
        :param tablename: Name of the table to create.
        :param csv_url: URL to the CSV file.
        """
        self.cache_minutes = cache_minutes
        self.tablename = tablename
        self.csv_url = csv_url
        self.last_refresh_time = 0
        self.engine = None
        self.conn = None  # This will store the single raw connection.
        self.refresh()

    def refresh(self):
        """Dispose of the old engine/connection (if any), create a new one using a StaticPool,
        load the CSV into a table, and store the raw connection."""
        if self.engine:
            # Close the existing raw connection if it's open.
            if self.conn:
                try:
                    self.conn.close()
                except Exception:
                    pass
            self.engine.dispose()

        # Create a new in‑memory DuckDB engine using a StaticPool.
        self.engine = create_engine(
            "duckdb:///:memory:",
            poolclass=StaticPool,
        )
        # Get a raw connection once and store it.
        self.conn = self.engine.raw_connection()

        # Create the table by loading the CSV.
        cur = self.conn.cursor()
        cur.execute(f"""
            CREATE TABLE {self.tablename} AS 
            SELECT * FROM read_csv_auto('{self.csv_url}')
        """)
        # Commit the changes so that they are visible.
        self.conn.commit()

        self.last_refresh_time = time.time()

    def get_connection(self):
        """Return the stored raw DBAPI connection. Refresh the engine if the cache lifetime has expired."""
        if (self.cache_minutes > 0) and (time.time() - self.last_refresh_time > self.cache_minutes * 60):
            self.refresh()
        return self.conn

########################################################################
# 2. The Dialect
########################################################################
# This dialect class implements the “livecsv” dialect. It does the following:
#
# - In create_connect_args(), it parses the URL parts.
#   Expected URL format:
#
#       livecsv://<ssl_mode>/<cache_minutes>/<tablename>/<csv_url>
#
#   For example, with:
#
#       livecsv://secure/10/customers/user:pass@www.google.com:443/peoples.csv
#
#   the components are:
#
#       ssl_mode    = "secure"    (if “secure” then SSL/https, otherwise plain http)
#       cache_minutes = 10         (CSV will be re‑loaded after 10 minutes)
#       tablename   = "customers" (the name of the table to be created)
#       csv_url     = "user:pass@www.google.com:443/peoples.csv"
#
#   If the csv_url does not already start with "http", it is prepended with
#   "https://" (if ssl_mode is “secure”) or "http://" (otherwise).
#
# - In do_connect(), it creates (if needed) a MyCSVConnectionProvider
#   and returns a DBAPI connection from it.
#
# - The dbapi() class method returns the duckdb module.
########################################################################

class LiveCSVDialect(default.DefaultDialect):
    name = "livecsv"
    driver = "duckdb"
    supports_statement_cache = False
    
    def create_connect_args(self, url):
        """
        Parse a URL of the form:
            livecsv://<ssl_mode>/<cache_minutes>/<tablename>/<csv_url>
        For example:
            livecsv://secure/10/customers/user:pass@www.google.com:443/peoples.csv
        """
        # The "host" portion holds the SSL mode:
        ssl_mode = url.host  # Expected to be "secure" or "insecure"
        # The remainder of the URL’s path is split into parts.
        parts = [p for p in url.database.split("/") if p]
        if len(parts) < 3:
            raise ValueError("Invalid livecsv URL. Expected format: "
                             "livecsv://<ssl_mode>/<cache_minutes>/<tablename>/<csv_url>")
        try:
            cache_minutes = int(parts[0])
        except ValueError:
            raise ValueError("Cache minutes must be an integer")
        tablename = parts[1]
        csv_url_parts = parts[2:]
        csv_url = "/".join(csv_url_parts)
        # If csv_url does not start with 'http', prepend a scheme based on ssl_mode.
        if not csv_url.startswith("http"):
            if ssl_mode.lower() == "secure":
                csv_url = "https://" + csv_url
            else:
                csv_url = "http://" + csv_url

        # Save our parsed parameters on the dialect instance.
        self._mycsv_params = {
            "cache_minutes": cache_minutes,
            "tablename": tablename,
            "csv_url": csv_url,
            "ssl_mode": ssl_mode,
        }
        # We return an empty tuple (and dict) because our DBAPI connect
        # isn’t used directly.
        return ([], {})

    def connect(self, *cargs, **cparams):
        """
        This method is invoked by SQLAlchemy’s connection pool to obtain a
        DBAPI-level connection.
        """
        # Create the caching provider on first use.
        if not hasattr(self, "_mycsv_provider"):
            self._mycsv_provider = LiveCSVConnectionProvider(
                cache_minutes=self._mycsv_params["cache_minutes"],
                tablename=self._mycsv_params["tablename"],
                csv_url=self._mycsv_params["csv_url"]
            )
        # Return a raw DBAPI connection from the caching provider.
        return self._mycsv_provider.get_connection()

    @classmethod
    def import_dbapi(cls):
        # Return the DuckDB DBAPI module.
        return duckdb
    
    @classmethod
    def dbapi(cls):
         return cls.import_dbapi()
    
    def do_commit(self, dbapi_connection):
        try:
            dbapi_connection.commit()
        except duckdb.TransactionException as ex:
            if "no transaction is active" in str(ex):
                # Ignore the error if there's no active transaction.
                pass
            else:
                raise

    def do_rollback(self, dbapi_connection):
        try:
            dbapi_connection.rollback()
        except duckdb.TransactionException as ex:
            if "no transaction is active" in str(ex):
                # Ignore this error as well.
                pass
            else:
                raise

########################################################################
# 3. Register the Dialect
########################################################################
# This makes the dialect available using the URL scheme "mycsv"
########################################################################
def register_driver():
    registry.register("livecsv", __name__, "LiveCSVDialect")

if __name__ == "__main__":
    register_driver()
