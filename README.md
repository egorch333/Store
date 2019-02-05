# Store - интернет магазин на django

Online Store январь 2019


##Шпаргалка по командам

_установка зависимостей пакетов_

pip install -r req.txt

_заморозка_

pip freeze > req.txt

_создание новой миграции_

python manage.py makemigrations

_выполнение всех миграции_

python manage.py migrate

_активация виртуальной машины_

source venv3.5/bin/activate

_проникаю в проект и запускаю django server_

python manage.py runserver

_создание нового приложения в корне основного приложения_

python manage.py startapp app_name
