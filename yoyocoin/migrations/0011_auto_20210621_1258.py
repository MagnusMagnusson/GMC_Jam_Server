# Generated by Django 3.1.7 on 2021-06-21 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yoyocoin', '0010_auto_20210613_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='stock',
            field=models.CharField(max_length=10),
        ),
    ]