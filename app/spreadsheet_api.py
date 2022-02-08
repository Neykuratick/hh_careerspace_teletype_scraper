import os
import logging
import time
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from gspread import authorize
from gspread.exceptions import APIError

from app.models import Columns
from config import config

logger = logging.getLogger(' SPREADSHEETS ')
logger.setLevel(level=config.LOGGING_LEVEL)


def Create_Service(client_secret_file, api_service_name, api_version, scopes):
    cred = None

    creds_file = f'secret/token_{api_service_name}_{api_version}.json'

    if os.path.exists(creds_file):
        cred = Credentials.from_authorized_user_file(filename=creds_file, scopes=scopes)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            cred = flow.run_local_server()

        with open(creds_file, 'w') as token:
            token.write(str(cred.to_json()))

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        return service, cred
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


sheets_service, creds = Create_Service(
    'secret/secret.json',
    'sheets',
    'v4',
    ['https://www.googleapis.com/auth/spreadsheets']
)


class Sheet:
    columns: Columns

    def __init__(self, url: str):
        client = authorize(creds)
        spreadsheet = client.open_by_url(url)
        self.__worksheet = spreadsheet.get_worksheet(0)
        self.columns = self.__get_columns()

    def __get_columns(self) -> Columns:
        columns = {}
        for index, column in enumerate(self.__worksheet.row_values(1)):
            columns[f'{column}'] = index + 1

        return Columns(
            url=columns.get(config.COLUMN_ALIAS_URL),
            name=columns.get(config.COLUMN_ALIAS_NAME),
            info=columns.get(config.COLUMN_ALIAS_INFO),
            full_text=columns.get(config.COLUMN_ALIAS_FULLTEXT),
            contacts=columns.get(config.COLUMN_ALIAS_CONTACTS),
            salary=columns.get(config.COLUMN_ALIAS_SALARY),
            date_added=columns.get(config.COLUMN_ALIAS_DATEADDED)
        )

    def append_column(self, column: int, value: Any) -> int:
        column_values = self.__worksheet.col_values(column)
        last_row_index = len(column_values) + 1
        self.__worksheet.update_cell(last_row_index, column, value)
        return last_row_index

    def delete_row(self, index):
        self.__worksheet.delete_row(index)

    def check_integrity(self) -> bool:
        last_sheet_row_index = len(self.__worksheet.col_values(self.columns.date_added))

        for column_index, column in enumerate(self.__worksheet.row_values(1)):
            actual_column_index = column_index + 1
            last_row_index = len(self.__worksheet.col_values(actual_column_index))

            logger.debug(f"last row: {last_sheet_row_index}; last row of {column}: {last_row_index}")
            if last_sheet_row_index > last_row_index > 1 and last_sheet_row_index > 1:
                self.delete_row(last_sheet_row_index)
                if self.check_integrity():
                    return True
                else:
                    return False

        return True
