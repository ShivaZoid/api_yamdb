# Generated by Django 3.2 on 2023-01-09 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
