# Generated by Django 2.2.4 on 2019-08-19 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggested',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
