import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


DB_CONFIG = {
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "event_pipeline"),
}


def get_engine() -> Engine:
    db_url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(db_url)


def create_table(engine: Engine, sql_file_path: str) -> None:
    with open(sql_file_path, "r", encoding="utf-8") as file:
        init_sql = file.read()

    with engine.begin() as connection:
        connection.execute(text(init_sql))


def test_connection(engine: Engine) -> None:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1;"))
        print("DB connection test result:", result.scalar())


def insert_events(engine: Engine, events: list[dict]) -> None:
    insert_sql = text("""
        INSERT INTO events (
            event_id,
            user_id,
            event_type,
            event_time,
            page_url,
            product_id,
            amount,
            error_code
        )
        VALUES (
            :event_id,
            :user_id,
            :event_type,
            :event_time,
            :page_url,
            :product_id,
            :amount,
            :error_code
        )
    """)

    with engine.begin() as connection:
        connection.execute(insert_sql, events)


def count_events(engine: Engine) -> int:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM events;"))
        return result.scalar()


if __name__ == "__main__":
    engine = get_engine()
    test_connection(engine)
    create_table(engine, "init.sql")
    print("Table created successfully.")