# Generated by Django 3.2 on 2022-12-20 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0008_alter_title_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]
