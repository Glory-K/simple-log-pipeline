import time
from sqlalchemy import text

from db import get_engine, create_table, insert_events, count_events
from generator import generate_events
from analysis import (
    get_event_type_counts,
    get_hourly_event_trend,
    get_error_rate,
)
from visualize import (
    save_event_type_counts_chart,
    save_hourly_event_trend_chart,
)


def wait_for_db(max_retries: int = 10, delay: int = 3):
    for attempt in range(1, max_retries + 1):
        try:
            engine = get_engine()
            with engine.connect() as connection:
                connection.execute(text("SELECT 1;"))
            print("Database is ready.")
            return engine
        except Exception as e:
            print(f"DB connection failed (attempt {attempt}/{max_retries}): {e}")
            time.sleep(delay)

    raise RuntimeError("Database connection failed after multiple retries.")


def main():
    engine = wait_for_db()

    create_table(engine, "init.sql")

    events = generate_events(1000)
    print(f"Generated events: {len(events)}")

    insert_events(engine, events)
    print("Events inserted successfully.")

    total_count = count_events(engine)
    print(f"Total events in DB: {total_count}")

    event_type_counts_df = get_event_type_counts(engine)
    hourly_event_trend_df = get_hourly_event_trend(engine)
    error_rate_df = get_error_rate(engine)

    print("\n[Event Type Counts]")
    print(event_type_counts_df)

    print("\n[Hourly Event Trend]")
    print(hourly_event_trend_df.head(10))

    error_rate = error_rate_df.loc[0, "error_rate"]
    print("\n[Error Rate]")
    print(f"Error Rate: {error_rate:.2f}%")

    event_type_chart_path = save_event_type_counts_chart(event_type_counts_df)
    hourly_trend_chart_path = save_hourly_event_trend_chart(hourly_event_trend_df)

    print(f"\nSaved chart: {event_type_chart_path}")
    print(f"Saved chart: {hourly_trend_chart_path}")


if __name__ == "__main__":
    main()