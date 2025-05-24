import psutil
import time
import logging
from logging.handlers import RotatingFileHandler
import argparse

# --- Configuration ---
DEFAULT_LOG_FILE = "system_monitor.log"
DEFAULT_INTERVAL = 5  # seconds
DEFAULT_MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
DEFAULT_LOG_BACKUP_COUNT = 5

def setup_logger(log_file, max_bytes, backup_count):
    """Configures the logger for outputting performance data."""
    logger = logging.getLogger("SystemMonitor")
    logger.setLevel(logging.INFO)

    # Prevent multiple handlers if script is re-run in same session (e.g. in an IDE)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a rotating file handler
    handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count
    )
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Also log to console for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def get_cpu_usage():
    """Returns the current system-wide CPU utilization as a percentage."""
    # interval=1 means it will compare CPU times over 1 second.
    # A non-zero interval is recommended for accuracy.
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """Returns the current system-wide memory utilization as a percentage."""
    mem = psutil.virtual_memory()
    return mem.percent

def main():
    """Main function to monitor and log system performance."""
    parser = argparse.ArgumentParser(description="Monitor system CPU and memory usage.")
    parser.add_argument(
        "--log_file",
        type=str,
        default=DEFAULT_LOG_FILE,
        help=f"Path to the log file (default: {DEFAULT_LOG_FILE})",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL,
        help=f"Monitoring interval in seconds (default: {DEFAULT_INTERVAL})",
    )
    parser.add_argument(
        "--max_log_size",
        type=int,
        default=DEFAULT_MAX_LOG_SIZE,
        help=f"Maximum log file size in bytes before rotation (default: {DEFAULT_MAX_LOG_SIZE})",
    )
    parser.add_argument(
        "--log_backup_count",
        type=int,
        default=DEFAULT_LOG_BACKUP_COUNT,
        help=f"Number of backup log files to keep (default: {DEFAULT_LOG_BACKUP_COUNT})",
    )

    args = parser.parse_args()

    logger = setup_logger(args.log_file, args.max_log_size, args.log_backup_count)
    logger.info("System Performance Monitor started.")
    logger.info(f"Logging to: {args.log_file}")
    logger.info(f"Monitoring interval: {args.interval} seconds")
    logger.info(f"Max log size: {args.max_log_size} bytes")
    logger.info(f"Log backup count: {args.log_backup_count}")


    try:
        while True:
            cpu_usage = get_cpu_usage()
            memory_usage = get_memory_usage()

            log_message = f"CPU Usage: {cpu_usage:.2f}%, Memory Usage: {memory_usage:.2f}%"
            logger.info(log_message)

            time.sleep(args.interval)

    except KeyboardInterrupt:
        logger.info("System Performance Monitor stopped by user.")
        print("\nMonitoring stopped.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        print(f"An error occurred: {e}")
    finally:
        logging.shutdown()

if __name__ == "__main__":
    main()