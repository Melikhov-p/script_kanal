1. Создать проект на python (при написании использовался python 3.10.0)
2. Скопировать файлы с репозитория в свой проект.
3. Установить зависимости из requirements.txt с помощью команды pip install -r requirements.txt
4. Для доступа к таблицы Google sheets понадобиться .json файл с секртеным ключом сервисного аккаунта console.cloud.google.com, файл сохранить в папку с проектом, указать название файла в скрипте main.py на 15 строке вместо "SECRET_KEY.json"
5. Установить себе базу данных kanal_db.sql (PostgreSQL 14)
6. В скрипте request_db.py в строке 5 и 17 вместо USERNAME указать имя пользователя
7. Запустить основной скрипт с помощью команды python main.py

ссылка на репозиторий с одностраничным приложением django БЕЗ REACT: https://github.com/Melikhov-p/django_kanal (выводит таблицу из базы данных)
