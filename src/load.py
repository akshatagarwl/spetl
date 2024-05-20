import sqlite3
import logging

logger = logging.getLogger(__name__)


def write_to_sqlite(df):
    sqlite_filename = "data/data.sqlite"
    conn = sqlite3.connect(sqlite_filename)
    df.to_sql("website_data", conn, if_exists="replace", index=False)
    conn.commit()
    logger.info(f"data written to sqlite {sqlite_filename}")
