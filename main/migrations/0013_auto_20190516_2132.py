# Generated by Django 2.2.1 on 2019-05-17 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20190516_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailaddress',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='emailaddress',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
