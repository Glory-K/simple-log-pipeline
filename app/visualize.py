import os
import matplotlib.pyplot as plt
import pandas as pd


OUTPUT_DIR = "output"


def ensure_output_dir() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_event_type_counts_chart(df: pd.DataFrame) -> str:
    ensure_output_dir()

    output_path = os.path.join(OUTPUT_DIR, "event_type_counts.png")

    plt.figure(figsize=(8, 5))
    plt.bar(df["event_type"], df["event_count"])
    plt.title("Event Type Counts")
    plt.xlabel("Event Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path


def save_hourly_event_trend_chart(df: pd.DataFrame) -> str:
    ensure_output_dir()

    output_path = os.path.join(OUTPUT_DIR, "hourly_event_trend.png")

    plt.figure(figsize=(10, 5))
    plt.plot(df["event_hour"], df["event_count"], marker="o")
    plt.title("Hourly Event Trend")
    plt.xlabel("Event Hour")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path