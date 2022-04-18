import logging

import requests
import re
from bs4 import BeautifulSoup

from config import config
from app.models import Vacancy

logger = logging.getLogger(' CAREERSPACE ')
logger.setLevel(level=config.LOGGING_LEVEL)


class CareerSpace:
    def __init__(self):
        self.__soup = None
        self.__url = None

    def __get_salary(self) -> str:
        result = self.__soup.find("span", {"class": "price"})
        try:
            return "".join(re.findall("[0-9|-]+", result.text))
        except Exception as e:
            logger.critical(e)
            return config.DEFAULT_FOR_EMPTY

    def __get_name(self) -> str:
        result = self.__soup.find("h3", {"class": "j-d-h__title"})
        try:
            return ' '.join(result.text.split())  # removes multiple spaces
        except Exception as e:
            logger.critical(e)
            return config.DEFAULT_FOR_EMPTY

    def __get_info(self) -> str:
        result = self.__soup.find("div", {"class": "j-d-desc"})
        try:
            return result.text
        except Exception as e:
            logger.critical(e)
            return config.DEFAULT_FOR_EMPTY

    def __get_contacts(self) -> str:

        results = self.__soup.find_all("script")
        for result in results:
            if not result.string:
                continue

            if 'company_contact_value' not in result.string:
                continue

            job = result.string.split("job_id")[1]

            raw_contact_value = job.split("company_contact_value")
            raw_contact_type = job.split("company_contact_type")
            contacts_amount = len(raw_contact_value)

            contact = ""
            for i in range(1, contacts_amount):
                contact_value = raw_contact_value[i].split('"')[1]
                contact_type = raw_contact_type[i].split('"')[1]

                if 'telegram' in contact_type:
                    contact += f"telegram: @{contact_value}; "

                elif 'http' in contact_value:
                    better_contact_value = contact_value.replace('u002F', '').replace('\\', '/')
                    contact += f"website: {better_contact_value}; "

                elif '@' in contact_value:
                    contact += f"email: {contact_value}; "

                else:
                    contact += f"undefined: {contact_value}; "

            return contact[:-2]

    def get_vacancy(self, url: str) -> Vacancy:
        logger.debug(f"Processing url: {url}")
        request_result = requests.get(url)

        self.__soup = BeautifulSoup(request_result.text, 'html.parser')
        self.__url = url

        name = self.__get_name()
        info = self.__get_info()
        contacts = self.__get_contacts()
        salary = self.__get_salary()

        return Vacancy(
            url=self.__url,
            name=name,
            info=info,
            full_text=info,
            contacts=contacts,
            salary=salary
        )
