# Generated by Django 3.1.7 on 2021-10-27 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jam42_babel', '0007_auto_20211021_2248'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='highscore',
            index=models.Index(fields=['date'], name='jam42_babel_date_0565d9_idx'),
        ),
        migrations.AddIndex(
            model_name='highscore',
            index=models.Index(fields=['height'], name='jam42_babel_height_49bd93_idx'),
        ),
        migrations.AddIndex(
            model_name='highscore',
            index=models.Index(fields=['rooms'], name='jam42_babel_rooms_3ca105_idx'),
        ),
    ]
