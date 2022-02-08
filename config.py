import logging
from typing import Union, Optional
from pydantic import BaseSettings, Field


class Config(BaseSettings):
    LOGGING_LEVEL: Optional[Union[int, str]] = Field(default=logging.DEBUG)
    SPREADSHEET_URL: str
    VK_TOKEN: str
    DEFAULT_FOR_EMPTY: str
    POSTS_COUNT: Optional[int] = Field(default=50)
    LAST_POST_ID: Optional[int] = Field(default=None)  # Айди последнего нужного поста в группе

    COLUMN_ALIAS_URL: Optional[str] = Field(default='url')
    COLUMN_ALIAS_NAME: Optional[str] = Field(default='name')
    COLUMN_ALIAS_INFO: Optional[str] = Field(default='info')
    COLUMN_ALIAS_FULLTEXT: Optional[str] = Field(default='full_text')
    COLUMN_ALIAS_CONTACTS: Optional[str] = Field(default='contacts')
    COLUMN_ALIAS_SALARY: Optional[str] = Field(default='salary')
    COLUMN_ALIAS_DATEADDED: Optional[str] = Field(default='date_added')


config = Config()
