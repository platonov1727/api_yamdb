# Generated by Django 3.2 on 2022-12-19 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20221219_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
    ]
