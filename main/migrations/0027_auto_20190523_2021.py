# Generated by Django 2.2.1 on 2019-05-24 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_delete_emailrequest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gamebring',
            options={'ordering': ['game']},
        ),
    ]
