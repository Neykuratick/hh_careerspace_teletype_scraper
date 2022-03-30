import logging

from config import config
from app.driver import drive
import schedule
logging.basicConfig(level=config.LOGGING_LEVEL)


def main():
    try:
        schedule.every(30).minutes.do(drive)
        schedule.run_all(delay_seconds=10)

        while True:
            schedule.run_pending()
    except Exception as e:
        print(f'ERROR: {e}')
        return main()


if __name__ == "__main__":
    main()
