from sqlalchemy import text
from sqlalchemy.engine import Engine
import pandas as pd


def get_event_type_counts(engine: Engine) -> pd.DataFrame:
    query = text("""
        SELECT
            event_type,
            COUNT(*) AS event_count
        FROM events
        GROUP BY event_type
        ORDER BY event_count DESC;
    """)

    return pd.read_sql(query, engine)


def get_hourly_event_trend(engine: Engine) -> pd.DataFrame:
    query = text("""
        SELECT
            DATE_TRUNC('hour', event_time) AS event_hour,
            COUNT(*) AS event_count
        FROM events
        GROUP BY event_hour
        ORDER BY event_hour;
    """)

    return pd.read_sql(query, engine)


def get_error_rate(engine: Engine) -> pd.DataFrame:
    query = text("""
        SELECT
            ROUND(
                100.0 * SUM(CASE WHEN event_type = 'error' THEN 1 ELSE 0 END) / COUNT(*),
                2
            ) AS error_rate
        FROM events;
    """)

    return pd.read_sql(query, engine)