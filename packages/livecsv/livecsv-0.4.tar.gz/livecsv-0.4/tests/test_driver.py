import pytest
from sqlalchemy import create_engine, text, inspect
import livecsv

def test_livecsv_dialect():
    # Create an engine using the custom dialect.
    engine = create_engine(
        "livecsv://secure/10/usernames/support.staffbase.com/hc/en-us/article_attachments/360009197031/username.csv"
    )

    assert inspect(engine).get_table_names() == ['usernames']
    
    # Open a connection and execute the query.
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usernames LIMIT 1")).fetchall()

    # Assert that the query result matches the expected output.
    assert result == [('booker12', 9012, 'Rachel', 'Booker')]
