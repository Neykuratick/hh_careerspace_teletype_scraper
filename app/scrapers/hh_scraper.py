import logging

import requests
import re
from bs4 import BeautifulSoup

from config import config
from app.models import Vacancy

logger = logging.getLogger(' HEADHUNTER ')
logger.setLevel(level=config.LOGGING_LEVEL)


class HeadHunter:
    def __init__(self, url: str):
        logger.debug(f"Processing url: {url}")

        vacancy_id = re.findall("[0-9]+", url.split("vacancy/")[1])[0]
        self.__vacancy_json = requests.get(f"https://api.hh.ru/vacancies/{vacancy_id}").json()
        self.__url = url

    def __get_info(self) -> str:
        html = self.__vacancy_json.get("description")
        soup = BeautifulSoup(html, 'html.parser')
        return soup.text

    def get_vacancy(self) -> Vacancy:
        name = self.__vacancy_json.get("name")
        info = self.__get_info()
        contacts = self.__vacancy_json.get("contacts")
        salary = self.__vacancy_json.get("salary")

        return Vacancy(
            url=self.__url,
            name=name,
            info=info,
            full_text=info,
            contacts=contacts,
            salary=salary
        )
