# Generated by Django 3.1.7 on 2021-06-12 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yoyocoin', '0007_auto_20210609_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yoyocoin.company'),
        ),
    ]
