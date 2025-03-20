System Monitoring & Reporting Demo

A minimal Python script that periodically collects CPU, memory, and disk usage metrics, stores them in a SQLite database, and generates a summary report with a usage trend chart. This project showcases:

    System Resource Monitoring (using psutil)
    Database Storage (with sqlite3)
    Data Analysis & Visualization (with pandas & matplotlib)
    Automation (scheduling repeated data collection at a fixed interval)

Features

    Automated Data Collection
        Gathers CPU, memory, and disk usage every few seconds (configurable).
        Inserts each snapshot into a local SQLite database (system_metrics.db).

    Clean Exit & Reporting
        Stop the script anytime with Ctrl + C.
        Prints basic stats (count, mean, min, max, etc.) and plots usage trends over time.

    Lightweight & Portable
        No external services required – runs on any machine with Python 3.

Requirements

    Python 3.7+
    psutil for system metrics
    pandas for data manipulation
    matplotlib for plotting

Install these dependencies with:

pip install psutil pandas matplotlib

(SQLite is already included with Python.)
How to Use

    Clone or Download this repository (or save the script, e.g. system_monitor.py).

    Install Dependencies:

pip install psutil pandas matplotlib

Run the Script:

    python system_monitor.py

        The script will create (or connect to) system_metrics.db, set up a table called metrics, and start logging system usage at a fixed interval (INTERVAL_SECONDS, default: 5s).
        It will print usage readings in the console.

    Stop Monitoring:
        Press Ctrl + C (or equivalent interrupt signal).
        Upon exit, you’ll see a summary report (stats) and a line chart of CPU, memory, and disk usage over time.

Preview

[2025-01-01 12:00:00] CPU: 23.5%, Mem: 45.2%, Disk: 78.3%
[2025-01-01 12:00:05] CPU: 18.7%, Mem: 46.1%, Disk: 78.3%
... (ctrl+C to stop) ...
Stopping data collection...

=== Summary Statistics ===
       cpu_usage  memory_usage  disk_usage
count   20.000000     20.000000   20.000000
mean    15.230000     46.120000   78.250000
std      4.012586      1.106123    0.125990
min      9.800000     44.500000   78.100000
max     23.500000     48.300000   78.400000

A Matplotlib plot pops up, showing trends of CPU, memory, and disk usage over time.
Extensions

    Alerts: Add threshold-based alerts (e.g., CPU > 80%) via email, Slack, or logging.
    Network Stats: Include psutil.net_io_counters() to track network I/O.
    Distributed Monitoring: Modify the script to collect metrics from multiple servers (via SSH or other APIs).
    Web Dashboard: Build a simple Flask or Streamlit app to visualize real-time charts.
    Containerization: Run as a Docker container for easier deployment in production.

License

This project is available under the MIT License. Feel free to use and adapt it for your own monitoring needs!
