# Generated by Django 3.2 on 2022-12-20 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0005_alter_title_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='author',
        ),
        migrations.RemoveField(
            model_name='review',
            name='title',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]