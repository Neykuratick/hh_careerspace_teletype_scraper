import logging
from config import config
from app.driver import drive
import schedule
logging.basicConfig(level=config.LOGGING_LEVEL)


def main():
    # schedule.every(86400).seconds.do(drive)
    schedule.every().day.at("15:01").do(drive)  # time is in UTC (UTC+3 15:20 -> 12:20 UTC)
    # schedule.run_all(delay_seconds=10)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
