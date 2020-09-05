# Generated by Django 3.1.1 on 2020-09-05 10:37

from django.db import migrations, models
import movies.validators


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20200905_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=255, validators=[movies.validators.unique_movie_title]),
        ),
    ]
