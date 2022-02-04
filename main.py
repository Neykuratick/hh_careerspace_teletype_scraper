import logging
from config import config
from app.driver import drive

logging.basicConfig(level=config.LOGGING_LEVEL)


def run():
    drive()


if __name__ == "__main__":
    run()
