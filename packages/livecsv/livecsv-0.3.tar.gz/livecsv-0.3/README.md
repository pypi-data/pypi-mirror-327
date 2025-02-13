# livecsv

**livecsv** is a custom SQLAlchemy dialect that loads CSV data from a remote source into an in‑memory DuckDB instance with caching support. It is designed for read‑only use and allows you to query CSV data as if it were a relational table.

## Installation

Install livecsv using pip:

```bash
pip install livecsv
```

Dependencies

livecsv depends on the following packages:
•	SQLAlchemy
•	duckdb
•	duckdb_engine

These dependencies will be automatically installed when you install livecsv.

## Usage

The livecsv dialect lets you create a SQLAlchemy engine with a custom connection string that loads CSV data from a remote URL. The CSV is loaded into an in‑memory DuckDB instance, and the data is cached for a configurable number of minutes.

Connection String Format

The connection string format for livecsv is:

livecsv://<ssl_mode>/<cache_minutes>/<table_name>/<csv_url>

•	ssl_mode: Either secure (for HTTPS) or insecure (for HTTP).
•	cache_minutes: The number of minutes to cache the CSV data before refreshing. If 0, it is unlimited (not refreshed).
•	table_name: The name of the table that will be created in the in‑memory database.
•	csv_url: The URL to the CSV file (if the URL does not start with http, a scheme will be automatically prepended based on the ssl_mode).

## Example

Below is a sample code snippet that demonstrates how to use livecsv:

from sqlalchemy import create_engine, text

# Create an engine using the livecsv dialect.
engine = create_engine(
    "livecsv://secure/10/usernames/support.staffbase.com/hc/en-us/article_attachments/360009197031/username.csv"
)

# Query the table created from the CSV.
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usernames LIMIT 1")).fetchall()
    for row in result:
        print(row)

In this example, livecsv:
•	Loads the CSV from the specified URL.
•	Creates a table named usernames.
•	Caches the data for 10 minutes.
•	Allows you to query the data using SQLAlchemy.

## Testing with pytest

livecsv includes tests that can be run using pytest.

Steps to Run Tests
1.	Install pytest (if you haven’t already):

```bash
pip install pytest
```

2.	Run pytest
From the root of your project, run:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Eyal Rahmani
