import logging
import time
from typing import List

from gspread.exceptions import APIError

from app.assets.modeller import Vacancy
from app.careerspace_scraper import CareerSpace
from app.hh_scraper import HeadHunter
from app.teletype_scraper import Teletype
from app.assets.spreadsheet_api import Sheet
from app.assets.utils import get_post_urls
from config import config

logger = logging.getLogger(' DRIVER ')
logger.setLevel(level=config.LOGGING_LEVEL)


def upload_to_spreadsheet(vacancy: Vacancy, sheet: Sheet):
    logger.debug(f"Deploying: {vacancy.url}")
    last_row = -1

    try:
        last_row = sheet.append_column(sheet.columns.url, vacancy.url)
        last_row = sheet.append_column(sheet.columns.name, vacancy.name)
        last_row = sheet.append_column(sheet.columns.info, vacancy.info)
        last_row = sheet.append_column(sheet.columns.full_text, vacancy.full_text)
        last_row = sheet.append_column(sheet.columns.contacts, vacancy.contacts)
        last_row = sheet.append_column(sheet.columns.salary, vacancy.salary)
    except APIError as e:
        if 'exceeded' in str(e):
            logger.warning(e)
            time.sleep(61)

            sheet.delete_row(last_row) if last_row > 0 else None
            upload_to_spreadsheet(vacancy, sheet)


def drive_careerspace(urls: List[str]):
    sheet = Sheet(config.SPREADSHEET_URL)

    for url in urls:
        careerspace = CareerSpace(url)
        vacancy = careerspace.get_vacancy()
        upload_to_spreadsheet(vacancy, sheet)


def drive_hh(urls: List[str]):
    sheet = Sheet(config.SPREADSHEET_URL)

    for url in urls:
        hh = HeadHunter(url)
        vacancy = hh.get_vacancy()
        upload_to_spreadsheet(vacancy, sheet)


def drive_teletype(urls: List[str]):
    sheet = Sheet(config.SPREADSHEET_URL)

    for url in urls:
        teletype = Teletype(url)
        vacancy = teletype.get_vacancy()
        upload_to_spreadsheet(vacancy, sheet)


def drive():
    urls = get_post_urls(1)
    drive_hh(urls.hh)
    drive_teletype(urls.teletype)
    drive_careerspace(urls.careerspace)


def test():
    sheet = Sheet(config.SPREADSHEET_URL)

    # career = CareerSpace("https://careerspace.app/job/27106?utm_source=HSE")
    # vacancy = career.get_vacancy()
    # sheet.delete_row(2)
    vacancy = Vacancy(url="kek", name="lol", info="dada", full_text="go fuck", contacts=None, salary=None)
    upload_to_spreadsheet(vacancy, sheet)
