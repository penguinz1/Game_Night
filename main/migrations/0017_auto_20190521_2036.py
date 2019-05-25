# Generated by Django 2.2.1 on 2019-05-22 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_massemail_editor'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactNotificant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]