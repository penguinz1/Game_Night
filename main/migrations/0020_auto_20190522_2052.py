# Generated by Django 2.2.1 on 2019-05-23 00:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20190522_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='seen',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
