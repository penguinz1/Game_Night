# Generated by Django 2.2.1 on 2019-05-21 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20190521_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='massemail',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]