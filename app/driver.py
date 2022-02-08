import logging
import time
import pytz
from typing import List
from datetime import datetime, timedelta

from gspread.exceptions import APIError

from app.models import Vacancy
from app.scrapers.careerspace_scraper import CareerSpace
from app.scrapers.hh_scraper import HeadHunter
from app.scrapers.teletype_scraper import Teletype
from app.spreadsheet_api import Sheet
from app.utils import get_post_urls
from config import config

logger = logging.getLogger(' DRIVER ')
logger.setLevel(level=config.LOGGING_LEVEL)


def upload_to_spreadsheet(vacancy: Vacancy, sheet: Sheet):
    logger.debug(f"Deploying: {vacancy.url}")
    last_row = -1
    timestamp = (datetime.now(tz=pytz.timezone("Europe/Moscow"))).strftime("%Y.%m.%d, %H:%M")
    try:
        last_row = sheet.append_column(sheet.columns.date_added, timestamp)
        last_row = sheet.append_column(sheet.columns.url, vacancy.url)
        last_row = sheet.append_column(sheet.columns.name, vacancy.name)
        last_row = sheet.append_column(sheet.columns.info, vacancy.info)
        last_row = sheet.append_column(sheet.columns.full_text, vacancy.full_text)
        last_row = sheet.append_column(sheet.columns.contacts, vacancy.contacts)
        last_row = sheet.append_column(sheet.columns.salary, vacancy.salary)
    except APIError as e:
        logger.warning(e)
        time.sleep(61)

        sheet.delete_row(last_row) if last_row > 0 else None
        upload_to_spreadsheet(vacancy, sheet)


def drive_careerspace(urls: List[str], sheet: Sheet):
    for url in urls:
        careerspace = CareerSpace(url)
        vacancy = careerspace.get_vacancy()
        upload_to_spreadsheet(vacancy, sheet)


def drive_hh(urls: List[str], sheet: Sheet):
    for url in urls:
        hh = HeadHunter(url)
        vacancy = hh.get_vacancy()
        upload_to_spreadsheet(vacancy, sheet)


def drive_teletype(urls: List[str], sheet: Sheet):
    for url in urls:
        teletype = Teletype(url)
        vacancy = teletype.get_vacancy()
        upload_to_spreadsheet(vacancy, sheet)


def drive_other(urls: List[str], sheet: Sheet):
    for url in urls:
        vacancy = Vacancy(
            url=url,
            name=config.DEFAULT_FOR_EMPTY,
            info=config.DEFAULT_FOR_EMPTY,
            full_text=config.DEFAULT_FOR_EMPTY,
            contacts=config.DEFAULT_FOR_EMPTY,
            salary=config.DEFAULT_FOR_EMPTY
        )

        upload_to_spreadsheet(vacancy, sheet)


def drive():
    # for i in range(config.POSTS_COUNT):
    print(config.POSTS_COUNT)
    for i in range(config.POSTS_COUNT -1, -1, -1):
        logger.info(f"Scraping post index: {i}")

        urls = get_post_urls(i)
        sheet = Sheet(config.SPREADSHEET_URL)

        try:
            sheet.check_integrity()
        except APIError as e:
            logger.warning(e)
            time.sleep(61)
            sheet.check_integrity()

        drive_careerspace(urls.careerspace, sheet)
        drive_hh(urls.hh, sheet)
        drive_teletype(urls.teletype, sheet)
        drive_other(urls.other, sheet)

    logger.info("Done scraping")


def test():
    sheet = Sheet(config.SPREADSHEET_URL)

    # career = CareerSpace("https://careerspace.app/job/27106?utm_source=HSE")
    # vacancy = career.get_vacancy()
    # sheet.delete_row(2)
    vacancy = Vacancy(url="kek", name="lol", info="dada", full_text="go fuck", contacts=None, salary=None)
    upload_to_spreadsheet(vacancy, sheet)
