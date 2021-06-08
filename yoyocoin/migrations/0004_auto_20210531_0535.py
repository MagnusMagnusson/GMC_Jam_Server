# Generated by Django 3.1.7 on 2021-05-31 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yoyocoin', '0003_tweet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('code', models.CharField(max_length=5)),
                ('shares', models.DecimalField(decimal_places=2, max_digits=12)),
                ('mediaDrive', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=12)),
                ('basevalue', models.DecimalField(decimal_places=2, max_digits=12)),
                ('targetvalue', models.DecimalField(decimal_places=2, max_digits=12)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yoyocoin.company')),
            ],
        ),
        migrations.DeleteModel(
            name='Yoyocoin',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]