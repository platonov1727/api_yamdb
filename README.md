# Проект студентов Яндекс.Практикум АПИ Yandex Movie Data Base(YaMDB)

## Описание

Сервис Апи для того, чтобы собирать пользовательские оценки и комментарии на произведения различных категорий и жанров.

#### Подробная документация по адресу YOURHOST/redoc/

В redoc описанны все ендпоинты и их возможности с примерами запросов. И ожидаемые ответы.

#### Возможности

- JWT Аутентификация
- возможность ознакомиться с отзывами без аутентификации(но нельзя оставить отзыв и поставить оценку)
- Получение списка всех категорий и жанров, добавление и удаление.
- Пользователи могут самостоятельно зарегистрироваться через идентификацию по email
- Есть возможность назначить администратора, модератора

#### Технологии

- Django==3.2
- django-filter==22.1
- django-import-export==3.0.2
- djangorestframework==3.12.4
- djangorestframework-simplejwt==5.2.2
- PyJWT==2.1.0

со списком всех используемых библиотек можно ознакомиться в файлe requirements.txt

#### Запуск проекта в dev-режиме

```git clone <название репозитория>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
Load test data in django admin panel
python manage.py runserver```

#### Авторы

https://github.com/Shabanov010
https://github.com/platonov1727
https://github.com/mariarozhina