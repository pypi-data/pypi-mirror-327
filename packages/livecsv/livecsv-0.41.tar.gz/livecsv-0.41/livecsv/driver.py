from sqlalchemy.dialects import registry
from sqlalchemy.engine.url import URL
import time
import duckdb
import duckdb_engine
from typing import Tuple, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.engine import Connection

########################################################################
# 1. The Connection Provider
########################################################################
# This helper class creates (and re‑creates) an in‑memory DuckDB engine,
# loading the CSV into a table. It also implements a caching timeout.
#
# When a DBAPI‑level connection is requested, it returns a raw connection
# from the underlying DuckDB engine.
########################################################################

class LiveCSVConnectionProvider(duckdb_engine.ConnectionWrapper):
    def __init__(self, cache_minutes: int, tablename: str, csv_url: str) -> None:
        """
        :param cache_minutes: Cache lifetime in minutes. Zero means unlimited.
        :param tablename: Name of the table to create.
        :param csv_url: URL to the CSV file.
        """
        self.cache_minutes = cache_minutes
        self.tablename = tablename
        self.csv_url = csv_url
        self.last_refresh_time = time.time()
        super().__init__(self.create_connection())

    def create_connection(self) -> duckdb.DuckDBPyConnection:
        """Create and return a new connection with the CSV loaded into a table."""
        conn = duckdb.connect()
        conn.sql(f"""
            CREATE TABLE {self.tablename} AS 
            SELECT * FROM read_csv_auto('{self.csv_url}')
        """)
        return conn
    
    def refresh_connection(self) -> None:
        """Dispose of the old engine/connection if required and create a new one."""
        if (self.cache_minutes > 0) and (time.time() - self.last_refresh_time > self.cache_minutes * 60):
            self.close()
            super().__init__(self.create_connection())
            self.closed = False
            self.last_refresh_time = time.time()
    
    def cursor(self) -> duckdb_engine.CursorWrapper:
        self.refresh_connection()
        return super().cursor()

    def __getattr__(self, name: str) -> Any:
        self.refresh_connection()
        return super().__getattr__(name)

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

class LiveCSVDialect(duckdb_engine.Dialect):
    name = "livecsv"
    supports_statement_cache = False

    def create_connect_args(self, url: URL) -> Tuple[tuple, dict]:
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
        opts = {
            "cache_minutes": cache_minutes,
            "tablename": tablename,
            "csv_url": csv_url,
        }
        return ((), opts)

    def connect(self, *cargs, **cparams) -> "Connection":
        """
        This method is invoked by SQLAlchemy’s connection pool to obtain a
        DBAPI-level connection.
        """
        # cparams = opts (from create_connect_args)
        # Create the caching provider on first use.
        return LiveCSVConnectionProvider(**cparams)

########################################################################
# 3. Register the Dialect
########################################################################
# This makes the dialect available using the URL scheme "mycsv"
########################################################################
def register_driver() -> None:
    registry.register("livecsv", __name__, "LiveCSVDialect")

if __name__ == "__main__":
    register_driver()
