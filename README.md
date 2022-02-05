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

Дополнительные конфиги и их значения по умолчанию: <br>
```POSTS_COUNT=0``` Количество постов для парсинга, начиная с 0-го <br>
```LOGGING_LEVEL=logging.DEBUG``` Уровень логгирования <br>