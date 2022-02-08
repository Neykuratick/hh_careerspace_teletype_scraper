from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from config import config


class Vacancy(BaseModel):
    url: str
    name: Optional[str] = Field(default=config.DEFAULT_FOR_EMPTY)
    info: Optional[str] = Field(default=config.DEFAULT_FOR_EMPTY)
    full_text: Optional[str] = Field(default=config.DEFAULT_FOR_EMPTY)
    contacts: Optional[str] = Field(default=config.DEFAULT_FOR_EMPTY)
    salary: Optional[str] = Field(default=config.DEFAULT_FOR_EMPTY)

    class Config:
        validate_assignment = True
        allow_reuse = True

    @validator('contacts')
    def set_contacts(cls, contacts):
        return contacts or config.DEFAULT_FOR_EMPTY

    @validator('salary')
    def set_salary(cls, salary):
        return salary or config.DEFAULT_FOR_EMPTY


class UrlList(BaseModel):
    teletype: List[str]
    careerspace: List[str]
    hh: List[str]
    other: Optional[List[str]]


class Columns(BaseModel):
    url: int
    name: int
    info: int
    full_text: int
    contacts: int
    salary: int
    date_added: int
