# Generated by Django 3.1.7 on 2021-10-21 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jam42_babel', '0004_auto_20210829_1703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='highscore',
            old_name='score',
            new_name='height',
        ),
        migrations.AddField(
            model_name='highscore',
            name='platform',
            field=models.CharField(default='WINDOWS', max_length=10),
        ),
    ]
