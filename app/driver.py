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
        try:
            sheet.check_integrity()

            careerspace = CareerSpace(url)
            vacancy = careerspace.get_vacancy()
            upload_to_spreadsheet(vacancy, sheet)
        except Exception as e:
            logger.critical(e)


def drive_hh(urls: List[str], sheet: Sheet):
    for url in urls:
        try:
            sheet.check_integrity()

            hh = HeadHunter(url)
            vacancy = hh.get_vacancy()
            upload_to_spreadsheet(vacancy, sheet)
        except Exception as e:
            logger.critical(e)


def drive_teletype(urls: List[str], sheet: Sheet):
    for url in urls:
        try:
            sheet.check_integrity()

            teletype = Teletype(url)
            vacancy = teletype.get_vacancy()
            upload_to_spreadsheet(vacancy, sheet)
        except Exception as e:
            logger.critical(e)


def drive_other(urls: List[str], sheet: Sheet):
    for url in urls:
        try:
            sheet.check_integrity()
            vacancy = Vacancy(
                url=url,
                name=config.DEFAULT_FOR_EMPTY,
                info=config.DEFAULT_FOR_EMPTY,
                full_text=config.DEFAULT_FOR_EMPTY,
                contacts=config.DEFAULT_FOR_EMPTY,
                salary=config.DEFAULT_FOR_EMPTY
            )

            upload_to_spreadsheet(vacancy, sheet)
        except Exception as e:
            logger.critical(e)


def drive():
    for i in range(config.POSTS_COUNT):
        logger.info(f"Scraping post index: {i}")

        urls = get_post_urls(i)
        sheet = Sheet(config.SPREADSHEET_URL)

        drive_careerspace(urls.careerspace, sheet)
        drive_hh(urls.hh, sheet)
        drive_teletype(urls.teletype, sheet)
        drive_other(urls.other, sheet)

    logger.info("Done scraping")


def test():
    sheet = Sheet(config.SPREADSHEET_URL)
    vacancy = Vacancy(url="kek", name="lol", info="dada", full_text="go fuck", contacts=None, salary=None)
    upload_to_spreadsheet(vacancy, sheet)
