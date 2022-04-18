import logging
from typing import List

from app.scrapers.careerspace_scraper import CareerSpace
from app.scrapers.hh_scraper import HeadHunter
from app.scrapers.teletype_scraper import Teletype
from app.utils import get_post_urls, telegram_broadcast, stringify
from config import config

logger = logging.getLogger(' DRIVER ')
logger.setLevel(level=config.LOGGING_LEVEL)


class DriverHolder:
    def __init__(self, url_list, driver_object):
        self.driver = driver_object
        self.urls = url_list


def execute_driver(urls: List[str], driver):
    for url in urls:
        vacancy = driver.get_vacancy(url)
        telegram_broadcast(stringify(vacancy))


def drive():
    for i in range(config.POSTS_COUNT):
        logger.info(f"Scraping post index: {i}")

        urls = get_post_urls(i)

        drivers = (
            DriverHolder(urls.careerspace, CareerSpace()),
            DriverHolder(urls.hh, HeadHunter()),
            DriverHolder(urls.teletype, Teletype()),
        )

        for driver in drivers:
            execute_driver(driver.urls, driver.driver)

    logger.info("Done scraping")

