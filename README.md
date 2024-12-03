Запустить локольно:

    Клонирование:

mkdir referal_system
cd referal_system
git clone <SSH repo_url>

    Зависимости

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

    Создать БД
    Сделать миграции и создать супер пользователя

./manage.py migrate
./manage.py createsuperuser

    Запустить сервер

/manage.py runserver

    Запустить бота

/manage.py bot

    Документация Swagger

http://127.0.0.1:8000/swagger/

