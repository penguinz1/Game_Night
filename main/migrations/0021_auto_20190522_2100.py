# Generated by Django 2.2.1 on 2019-05-23 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20190522_2052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alert',
            options={'ordering': ['severity', 'time']},
        ),
        migrations.AlterModelOptions(
            name='massemail',
            options={'permissions': (('can_send_emails', 'Abilty to send club emails'),)},
        ),
    ]