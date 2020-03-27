# Store - интернет магазин на django

Online Store январь 2019


##Шпаргалка

_установка зависимостей пакетов_

pip install -r req.txt

_заморозка_

pip freeze > req.txt

_создание новой миграции_

python manage.py makemigrations

_выполнение всех миграции_

python manage.py migrate

_фейковые миграции после восстановления базы_

python manage.py migrate --fake

_активация виртуальной машины_

source venv3.5/bin/activate

_проникаю в проект и запускаю django server_

python manage.py runserver

_создание нового приложения в корне основного приложения_

python manage.py startapp app_name

_показ данных в json_

python manage.py dumpdata profiles

python manage.py dumpdata --format=xml

python manage.py dumpdata --format=json

_заходим в psql_

python manage.py dbshell

_показать миграции в виде списка_

python manage.py showmigrations -l

test
