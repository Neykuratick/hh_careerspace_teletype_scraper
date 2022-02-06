import logging

import requests
from bs4 import BeautifulSoup

from config import config
from app.models import Vacancy

logger = logging.getLogger(' TELETYPE ')
logger.setLevel(level=config.LOGGING_LEVEL)


class Teletype:
    def __init__(self, url: str):
        logger.debug(f"Processing url: {url}")
        request_result = requests.get(url)
        request_result.encoding = "utf-8"

        self.__soup = BeautifulSoup(request_result.text, 'html.parser')
        self.__url = url

    def __get_info(self):
        # text = ""
        # article = self.__soup.find('article')
        # for paragraph in article.find_all("p"):
        #     text += f"{paragraph.text} \n"

        # return text
        return self.__soup.find('article').text

    def __get_contacts(self):
        keywords = ["контакт ", "контакты", "отклик", "@"]
        contacts = ""

        article = self.__soup.find('article')
        for index, paragraph in enumerate(article):
            text = paragraph.text.lower()
            href_tag = paragraph.find('a', href=True)

            if href_tag:
                url = href_tag['href']
                contacts += f"website: {url}; " if 'mailto' not in url else ''

            if any(trigger in text for trigger in keywords):
                contacts += f"{paragraph.text}; "

            elif index == len(article) - 1:
                contacts += f"{paragraph.text}; "

        return contacts

    def get_vacancy(self):
        name = self.__soup.find('title').text
        info = self.__get_info()
        contacts = self.__get_contacts()

        return Vacancy(
            url=self.__url,
            name=name,
            info=info,
            full_text=info,
            contacts=contacts,
            salary=None
        )
