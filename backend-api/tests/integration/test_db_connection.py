import os
import sqlalchemy


def test_db_connection():
    url = os.environ.get("DATABASE_URL") or os.environ.get("TEST_DATABASE_URL")
    assert url, "Set DATABASE_URL or TEST_DATABASE_URL in CI"
    engine = sqlalchemy.create_engine(url)
    with engine.connect() as conn:
        r = conn.execute(sqlalchemy.text("SELECT 1")).scalar()
    assert int(r) == 1
