# Generated by Django 3.1.7 on 2021-08-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='highScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=99)),
                ('mode', models.CharField(max_length=7)),
                ('score', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
