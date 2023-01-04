# Project Yamdb
![](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

## Authors
  - [Ayur Cybenov](https://github.com/ShivaZoid/)
  - [Alekseev Maksim](https://github.com/xodiumx)
  - [Sergey Kryukov](https://github.com/HomeGreyHome)
  
## Description
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Добавлять произведения, категории и жанры может только администратор. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); Пользователи могут оставлять комментарии к отзывам. Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

#### Реализованы следующие возможности:
  - Регистрация пользователя, с подтверждением через email
  - Аутентификация пользователя через JWT
  - 
  -
  -
## Как развернуть проект
- Клонируйте данный репозиторий на свой компьютер
```
git clone https://github.com/ShivaZoid/api_yamdb
```
- Cоздать и активировать виртуальное окружение:
```
py -3.10 -m venv venv
```
- Активировать venv
```
source venv/Scripts/activate или source env/bin/activate для mac
```
- Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
- Выполнить миграции:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
- Запустить проект из директории где находится файл manage.py:
```
python manage.py runserver
```

## TODO Example
** GET
** POST
** DALETE
