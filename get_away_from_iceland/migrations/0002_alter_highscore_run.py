# Generated by Django 4.2.1 on 2023-06-05 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_away_from_iceland', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highscore',
            name='run',
            field=models.TextField(max_length=4000),
        ),
    ]
