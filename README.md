# IDZ4_restaurant

Для решения данной задачи были использованы Python + Flask и БД PostgreSQL. 
Postman-коллекция экспортирована в файл Restaurant.postman_collection.json

### Файлы
Для запуска и тестирования программы необходимо отредактировать файл config.py в соответствии с базой данных и сетевыми настройками.

Файл create_tables.py позволяет создать необходимы для задания таблицы users и sessions.

Файл delete_tables.py позволяет удалить эти две таблицы.

Файл fill_in_the_tables.py позволяет предварительно заполнить таблицу users двумя записями.

В файле SQL_queries.py прописаны запросы к базе данных, используемые в коде.

В файле DB_functions.py прописаны функции для работы с базой данных, используемые потом в основном файле программы.

Основной файл с кодом - main.py, в нём кодируется само REST API.

### Endpoint-ы и запросы к ним
Примеры запросов для лучшего понимания можно посмотреть в Postman-коллекции.

Во всех запросах необходимо подавать данные на вход в формате JSON.

1) Регистрация: POST /api/registration

{
	"username": "ALex",
	"email": "alex@mail.ru",
	"password": "qwerty",
  "role": "chef"
}

2) Авторизация: POST /api/authorization

{
	"email": "alex@mail.ru",
	"password": "qwerty"
}

3) Получение информации о пользователе: GET /api/user_info

{
"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4Njc4NjIzMSwianRpIjoiMWYyY2M5NWUtOTcwYi00MWZmLTlkZGItNDIwZDgxZmM4ZjdiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MTIsIm5iZiI6MTY4Njc4NjIzMSwiZXhwIjoxNjg4ODU5ODMxfQ.shAJUPEJqSVbGQ09eFmN1veQLnf9qfJv2P9N3CTfwqs"
}


В ответ на экран выводятся необходимые сообщения и коды состояний REST.
