# Generated by Django 2.2.1 on 2019-05-15 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20190514_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteOfDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.CharField(max_length=500)),
                ('speaker', models.CharField(max_length=200)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoOfDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('visible_text', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]