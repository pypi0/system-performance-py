# System Performance Monitor Tutorial

This tutorial explains how to use the `main.py` script to monitor your system's CPU and memory usage, and log the results to a file.

## Prerequisites

Before running the script, make sure you have Python installed and install the required package:

```bash
pip install psutil
```

## Script Overview

The script monitors system CPU and memory usage at regular intervals and logs the data to a rotating log file. It uses the following main components:

- **psutil**: For accessing system performance data.
- **logging**: For logging performance data to a file and the console.
- **argparse**: For parsing command-line arguments.

## Usage

Run the script from the terminal:

```bash
python main.py
```

### Command-Line Arguments

You can customize the script using these optional arguments:

- `--log_file`: Path to the log file (default: `system_monitor.log`)
- `--interval`: Monitoring interval in seconds (default: `5`)
- `--max_log_size`: Maximum log file size in bytes before rotation (default: `10485760` for 10 MB)
- `--log_backup_count`: Number of backup log files to keep (default: `5`)

**Example:**

```bash
python main.py --interval 2 --log_file mylog.log --max_log_size 2097152 --log_backup_count 3
```

## How It Works

1. **Logger Setup**:  
   The script sets up a logger that writes to both a file (with rotation) and the console.

2. **Monitoring Loop**:  
   In an infinite loop, the script:
   - Measures CPU usage (`psutil.cpu_percent(interval=1)`)
   - Measures memory usage (`psutil.virtual_memory().percent`)
   - Logs the results
   - Waits for the specified interval

3. **Graceful Shutdown**:  
   If you press `Ctrl+C`, the script logs a shutdown message and exits cleanly.

## Example Log Output

```
2025-05-24 12:00:00,000 - INFO - CPU Usage: 12.34%, Memory Usage: 45.67%
2025-05-24 12:00:05,001 - INFO - CPU Usage: 10.21%, Memory Usage: 45.80%
```

## Customization

You can modify the script to log additional system metrics by adding new functions using `psutil`.

---

For more details, see the comments in `main.py`.