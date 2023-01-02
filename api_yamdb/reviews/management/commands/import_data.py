import csv

from django.core.management.base import BaseCommand

from reviews import models
from users.models import User

models_assignments = {
    'users': User,
    'titles': models.Title,
    'category': models.Category,
    'genre': models.Genre,
    'genre_title': models.TitleGenre,
    'review': models.Review,
    'comments': models.Comment,
}

# имена в csv для связей с внешними ключами
# key - имя csv-файла
# value - кортеж вариантов имен в столбцах таблицы csv
fk_names = {
    'category': ('category_id', 'category'),
    'users': ('author', 'users', 'author_id', 'user_id', ),
}


class Command(BaseCommand):
    """
    Загрузка данных в базу данных из CSV-файла.
    """

    def handle(self, *args, **options):
        if models.Title.objects.exists():
            print('В базе уже есть данные')
            return

        table_names = list(models_assignments.keys())
        for table in table_names:
            csv_file = f'static/data/{table}.csv'
            with open(csv_file, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    model = models_assignments.get(table)
                    for key in row.keys():
                        for item in fk_names.items():
                            if key in item[1]:
                                fk_model = models_assignments[item[0]]
                                fk_inst = fk_model.objects.get(
                                    pk=int(row[key])
                                )
                                row[key] = fk_inst
                    model.objects.update_or_create(**row)
            print(f'Загрузка "{table}" выполнена')
        print('Загрузка завершена')
