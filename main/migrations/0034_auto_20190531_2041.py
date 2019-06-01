# Generated by Django 2.2.1 on 2019-06-01 01:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_gameofweek_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='message',
            field=models.CharField(help_text='Enter an alert message (max 250 characters).', max_length=250),
        ),
        migrations.AlterField(
            model_name='alert',
            name='seen',
            field=models.ManyToManyField(blank=True, help_text='List of users who have seen the alert. Leave blank if creating an alert.', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='alert',
            name='severity',
            field=models.CharField(choices=[('1m', 'Message'), ('2a', 'Alert'), ('3w', 'Warning')], help_text='Determines the severity of the alert (which changes the banner appearance).', max_length=2),
        ),
        migrations.AlterField(
            model_name='alert',
            name='time',
            field=models.DateTimeField(help_text='Enter the time and date when the alert should expire.'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, help_text='The email address of the contact request sender (optional)', max_length=254, null=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.CharField(help_text='The message of the contact request.', max_length=500),
        ),
        migrations.AlterField(
            model_name='contact',
            name='seen',
            field=models.BooleanField(default=False, help_text='A flag indicating whether the club officers have seen this contact request.'),
        ),
        migrations.AlterField(
            model_name='contactnotificant',
            name='email',
            field=models.EmailField(help_text='An email address of an officer wating to receive contact requests.', max_length=254),
        ),
        migrations.AlterField(
            model_name='emailaddress',
            name='email',
            field=models.EmailField(help_text='The email address of a Game Night member.', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='emailaddress',
            name='name',
            field=models.CharField(help_text='The name attached to the email address.', max_length=200),
        ),
        migrations.AlterField(
            model_name='gamebring',
            name='game',
            field=models.CharField(help_text='Enter the game to be brought (max 100 characters).', max_length=100),
        ),
        migrations.AlterField(
            model_name='gamebring',
            name='meeting',
            field=models.ForeignKey(help_text='The meeting to which the game will be attached.', on_delete=django.db.models.deletion.CASCADE, to='main.Meeting'),
        ),
        migrations.AlterField(
            model_name='gamebring',
            name='person',
            field=models.CharField(blank=True, help_text='Enter the name of the person bringing the game (optional).', max_length=180, null=True),
        ),
        migrations.AlterField(
            model_name='gameofweek',
            name='game',
            field=models.CharField(help_text='The name of the game of the week (max 100 characters).', max_length=100),
        ),
        migrations.AlterField(
            model_name='gameofweek',
            name='image',
            field=models.ImageField(help_text='The image of the game of the week (most file formats work, please try to keep the file small).', upload_to=''),
        ),
        migrations.AlterField(
            model_name='gameofweek',
            name='time',
            field=models.DateTimeField(help_text='The time and date the game will be shown.'),
        ),
        migrations.AlterField(
            model_name='gamescore',
            name='drifters',
            field=models.PositiveIntegerField(help_text='The number of drifters destroyed by the player after finishing a round of the space game.'),
        ),
        migrations.AlterField(
            model_name='gamescore',
            name='player',
            field=models.ForeignKey(blank=True, help_text='The player of the round of the space game', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gamescore',
            name='score',
            field=models.PositiveIntegerField(help_text='The score of the player after finishing a round of the space game.'),
        ),
        migrations.AlterField(
            model_name='gamescore',
            name='time',
            field=models.DateTimeField(auto_now_add=True, help_text='The time the player finished a round of the space game.'),
        ),
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.FloatField(help_text='The latitude in degrees (must be between -90 and 90).', validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)]),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.FloatField(help_text='The longitude in degrees (must be between -180 and 180).', validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)]),
        ),
        migrations.AlterField(
            model_name='location',
            name='place',
            field=models.CharField(help_text='The name of the location.', max_length=200),
        ),
        migrations.AlterField(
            model_name='massemail',
            name='content',
            field=models.CharField(help_text='The HTML content for the mass email.', max_length=2000),
        ),
        migrations.AlterField(
            model_name='massemail',
            name='editor',
            field=models.ForeignKey(blank=True, help_text='The user who last edited the mass email.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='massemail',
            name='is_sent',
            field=models.BooleanField(default=False, help_text='A flag indicating whether the mass email was sent out.'),
        ),
        migrations.AlterField(
            model_name='massemail',
            name='last_edit',
            field=models.DateTimeField(auto_now_add=True, help_text='The time of the last edit of the mass email.'),
        ),
        migrations.AlterField(
            model_name='massemail',
            name='subject',
            field=models.CharField(help_text='The subject line for the mass email (max 200 characters).', max_length=200),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='email',
            field=models.OneToOneField(blank=True, help_text='The mass email that is attached to this meeting. Leave blank when creating a new meeting.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.MassEmail'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='location',
            field=models.ForeignKey(help_text='The location of the meeting.', on_delete=django.db.models.deletion.CASCADE, to='main.Location'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='name',
            field=models.CharField(blank=True, help_text='A custom name for the meeting (optional, max 100 characters).', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time',
            field=models.DateTimeField(help_text='The date and time of the meeting.'),
        ),
        migrations.AlterField(
            model_name='quoteofday',
            name='quote',
            field=models.CharField(help_text='The quote of the day (max 500 characters).', max_length=500),
        ),
        migrations.AlterField(
            model_name='quoteofday',
            name='speaker',
            field=models.CharField(help_text='The speaker of the quote.', max_length=200),
        ),
        migrations.AlterField(
            model_name='quoteofday',
            name='time',
            field=models.DateTimeField(help_text='The time and date the quote will be shown.'),
        ),
        migrations.AlterField(
            model_name='videoofday',
            name='description',
            field=models.CharField(blank=True, help_text='A description of the video (optional).', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='videoofday',
            name='link',
            field=models.CharField(help_text='The link to the video of the day.', max_length=1000),
        ),
        migrations.AlterField(
            model_name='videoofday',
            name='time',
            field=models.DateTimeField(help_text='The time and date the video will be shown.'),
        ),
        migrations.AlterField(
            model_name='videoofday',
            name='visible_text',
            field=models.CharField(help_text='The front page text that will contain the video link.', max_length=500),
        ),
    ]
