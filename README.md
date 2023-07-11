# django-marketplace

## Описание
Проект написан в ходе учебы, представляет собой набор API-эндпоинтов, их логику, кастомную админку и все это для готового фронтэнда, который предоставляет SkillBox

## Установка

### Frontend
Для установки нужно перейти в папку `diploma-frontend` и следовать инструкциям из файла `README.md`

### Backend

Для установки нужно установить все нужные пакеты командой `pip install -r requirements.txt`

Создать в корне папки marketplace файл `.env` и указать в нем секретный ключ

`SECRET_KEY='django-insecure-gg$g5o9m0jjpz2gu*h&fs62i97(2m_7ky9q4!6dt*i2)9ol^@='`

Далее нужно создать и применить миграции командами `python manage.py makemigrations` и `python manage.py migrate`, при возникновении ошибки во время применения миграций следует указать флаг --fake 
`python manage.py migrate --fake`

Для наглядности в проекте присутствуют фикстуры, устанавливать их следует в таком порядке:

`python manage.py loaddata app_users/fixtures/initial_data.json`

`python manage.py loaddata app_shop/fixtures/initial_data.json`


## Используемые библиотеки 


+ Django 4.2.1
+ Django Rest Framework 3.14.0
+ django-filter 23.2
+ django-phonenumber-field 7.1.0
+ Pillow 9.5.0
+ python-dotenv 1.0.0




