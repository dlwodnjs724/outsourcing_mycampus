# Generated by Django 2.2.4 on 2019-08-20 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0002_auto_20190819_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(db_column='object_id')),
                ('what', models.TextField(max_length=500)),
                ('content_type', models.ForeignKey(db_column='content_type_id', on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]