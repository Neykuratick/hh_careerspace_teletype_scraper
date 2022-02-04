Деплой:

Указать значения в файле .env в корне приложения:

`SPREADSHEET_URL=Some_String` str, ссылка на таблицу гугл <br>
`VK_TOKEN=Some_String ` str, либо сервисный, либо личный токен вконтакте<br>
`DEFAULT_FOR_EMPTY=Some_String `  str, тут любая строка-заглушка для недостающих данных<br>

Ещё в .env можно указать алиасы для столбиков в таблице. По умолчанию, значения следующие:
`COLUMN_ALIAS_URL=url` <br>
`COLUMN_ALIAS_NAME=name` <br>
`COLUMN_ALIAS_INF=info` <br>
`COLUMN_ALIAS_FULLTEXT=full_text `<br>
`COLUMN_ALIAS_CONTACTS=contacts `<br>
`COLUMN_ALIAS_SALARY=salary` <br>