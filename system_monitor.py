#!/usr/bin/env python
"""
System Monitoring Demo:
1. Collects CPU, memory, disk usage, and timestamps at a fixed interval.
2. Stores metrics in a local SQLite database.
3. Provides simple analytics and a Matplotlib chart to visualize usage trends.
"""

import time
import sqlite3
import psutil
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DB_NAME = "system_metrics.db"
INTERVAL_SECONDS = 5  # how often to collect metrics

def init_db(conn):
    """
    Creates a 'metrics' table if it doesn't already exist.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        cpu_usage FLOAT NOT NULL,
        memory_usage FLOAT NOT NULL,
        disk_usage FLOAT NOT NULL
    );
    """
    conn.execute(create_table_query)
    conn.commit()

def collect_metrics(conn):
    """
    Collects CPU, memory, and disk usage using psutil.
    Inserts a record into the 'metrics' table with a timestamp.
    """
    cpu_usage = psutil.cpu_percent(interval=None)
    mem_info = psutil.virtual_memory()
    memory_usage = mem_info.percent
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent

    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    insert_query = """
    INSERT INTO metrics (timestamp, cpu_usage, memory_usage, disk_usage)
    VALUES (?, ?, ?, ?);
    """
    conn.execute(insert_query, (timestamp_str, cpu_usage, memory_usage, disk_usage))
    conn.commit()

    print(f"[{timestamp_str}] CPU: {cpu_usage}%, Mem: {memory_usage}%, Disk: {disk_usage}%")

def generate_report(conn):
    """
    Loads all metrics from the database, prints out summary stats,
    and plots CPU/Memory/Disk usage trends over time.
    """
    df = pd.read_sql_query("SELECT * FROM metrics ORDER BY timestamp;", conn)
    
    if df.empty:
        print("No data collected yet.")
        return

    # Convert timestamp string to a datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Basic stats
    print("\n=== Summary Statistics ===")
    print(df[['cpu_usage', 'memory_usage', 'disk_usage']].describe())
    
    # Plot usage over time
    plt.figure(figsize=(10,5))
    plt.plot(df['timestamp'], df['cpu_usage'], label='CPU Usage')
    plt.plot(df['timestamp'], df['memory_usage'], label='Memory Usage')
    plt.plot(df['timestamp'], df['disk_usage'], label='Disk Usage')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Usage (%)')
    plt.title('System Resource Usage Over Time')
    plt.tight_layout()
    plt.show()

def main():
    """
    - Initializes the database and table.
    - Repeatedly collects metrics every INTERVAL_SECONDS.
    - Exits on KeyboardInterrupt, then generates a report.
    """
    with sqlite3.connect(DB_NAME) as conn:
        # 1. Set up table
        init_db(conn)

        try:
            print(f"Starting system monitoring every {INTERVAL_SECONDS} seconds. Press Ctrl+C to stop.")
            while True:
                collect_metrics(conn)
                time.sleep(INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\nStopping data collection...")

        # 2. Generate final report
        generate_report(conn)

if __name__ == "__main__":
    main()
