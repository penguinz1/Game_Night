from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver

from accounts.models import User
# Create your models here.

class GameScore(models.Model):
    """Model to store points for a round of the space game."""
    score    = models.PositiveIntegerField(
        help_text = "The score of the player after finishing a round of the space game.")
    drifters = models.PositiveIntegerField(
        help_text = "The number of drifters destroyed by the player after finishing a round of the space game.")
    time     = models.DateTimeField(auto_now_add = True,
        help_text = "The time the player finished a round of the space game.")
    player   = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True,
        help_text = "The player of the round of the space game")

    def __str__(self):
        """String for representing the Model object."""
        if (self.player):
            return f'{self.player.username} - {self.score}'
        else:
            return f'anonymous - {self.score}'


class Alert(models.Model):
    """Model for setting website banner alerts."""
    MESSAGE = '1m'
    ALERT   = '2a'
    WARNING = '3w'
    SEVERITY_CHOICES = (
        (MESSAGE, 'Message'),
        (ALERT, 'Alert'),
        (WARNING, 'Warning'),
    )

    message  = models.CharField(max_length = 500,
        help_text = "Enter an alert message (max 500 characters).")
    time     = models.DateTimeField(
        help_text = "Enter the time and date when the alert should expire.")
    seen     = models.ManyToManyField(User, blank = True,
        help_text = "List of users who have seen the alert. Leave blank if creating an alert.")
    severity = models.CharField(max_length = 2, choices = SEVERITY_CHOICES, default = ALERT, 
        help_text = "Determines the severity of the alert (which changes the banner appearance).")

    class Meta:
        """Ordering of the Model objects."""
        ordering = ['-severity', 'time']

    def __str__(self):
        """String for representing the Model object."""
        return self.message


class GameBring(models.Model):
    """Model to represent games that members will bring."""
    game    = models.CharField(max_length = 100,
        help_text = "Enter the game to be brought (max 100 characters).")
    person  = models.CharField(max_length = 180, blank = True, null = True,
        help_text = "Enter the name of the person bringing the game (optional).")
    meeting = models.ForeignKey('Meeting', on_delete = models.CASCADE,
        help_text = "The meeting to which the game will be attached.")

    class Meta:
        """Ordering of the Model objects."""
        ordering = ['game']

    def __str__(self):
        """String for representing the Model object."""
        if (self.person):
            return f'{self.person} - {self.game}'
        else:
            return f'anonymous - {self.game}'


class Meeting(models.Model):
    """Model to represent Game Night meetings."""
    time     = models.DateTimeField(
        help_text = "The date and time of the meeting.")
    name     = models.CharField(max_length = 100, blank = True, null = True,
        help_text = "A custom name for the meeting (optional, max 100 characters).")
    location = models.ForeignKey('Location', on_delete = models.CASCADE,
        help_text = "The location of the meeting.")
    email    = models.OneToOneField('MassEmail', on_delete = models.SET_NULL, blank = True, null = True,
        help_text = "The mass email that is attached to this meeting. Leave blank when creating a new meeting.")

    class Meta:
        """Ordering of the Model objects."""
        ordering = ['time']

    def __str__(self):
        """String for representing the Model object."""
        if (self.name):
            return f'{self.name} - {self.time}'
        else:
            return f'{self.time}'

class MassEmail(models.Model):
    """Model to represent Game Night weekly emails."""
    subject   = models.CharField(max_length = 200,
        help_text = "The subject line for the mass email (max 200 characters).")
    content   = models.CharField(max_length = 2000,
        help_text = "The HTML content for the mass email.")
    last_edit = models.DateTimeField(
        help_text = "The time of the last edit of the mass email.")
    editor    = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True,
        help_text = "The user who last edited the mass email.")
    is_sent   = models.BooleanField(default = False,
        help_text = "A flag indicating whether the mass email was sent out.")

    class Meta:
        """Permissions belonging to the Model objects."""
        permissions = (('can_send_emails', 'Abilty to send club emails'),)
        ordering = ['last_edit']

    def __str__(self):
        """String for representing the Model object."""
        return self.subject;

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.last_edit = timezone.now()
        return super(MassEmail, self).save(*args, **kwargs)


class Location(models.Model):
    """Model to represent locations of Game Night meetings."""
    place = models.CharField(max_length = 200,
        help_text = "The name of the location.")
    latitude = models.FloatField(validators = [MinValueValidator(-90), MaxValueValidator(90)],
        help_text = "The latitude in degrees (must be between -90 and 90). " +
            "For help on finding the latitude and longitude, see [https://support.google.com/maps/answer/18539].")
    longitude = models.FloatField(validators = [MinValueValidator(-180), MaxValueValidator(180)],
        help_text = "The longitude in degrees (must be between -180 and 180)." +
            "For help on finding the latitude and longitude, see [https://support.google.com/maps/answer/18539].")

    def __str__(self):
        """String fo representing the Model object."""
        return self.place


class Contact(models.Model):
    """Model to store outside contact requests."""
    message = models.CharField(max_length = 500,
        help_text = "The message of the contact request.")
    email   = models.EmailField(blank = True, null = True, max_length = 254, verbose_name = 'email address',
        help_text = "The email address of the contact request sender (optional).")
    time = models.DateTimeField(auto_now_add = True,
        help_text = "Time and date when the contact request was created.")
    seen    = models.BooleanField(default = False,
        help_text = "A flag indicating whether the club officers have seen this contact request.")

    class Meta:
        """Ordering of the Model objects."""
        ordering = ['seen', 'time']

    def __str__(self):
        return self.message

class ContactNotificant(models.Model):
    """Model to store emails of officers wanting to receive contact requests."""
    email = models.EmailField(
        help_text = "An email address of an officer wanting to receive contact requests.")

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.email}'

class QuoteOfDay(models.Model):
    """Model to store front page quotes"""
    quote = models.CharField(max_length = 500,
        help_text = "The quote of the day (max 500 characters).")
    speaker = models.CharField(max_length = 200,
        help_text = "The speaker of the quote.")
    time = models.DateTimeField(
        help_text = "The time and date the quote will be shown.")

    class Meta:
        """Ordering of the Model objects."""
        ordering = ['-time']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.speaker} - {self.quote}'

class VideoOfDay(models.Model):
    """Model to store front page video links."""
    link = models.CharField(max_length = 1000,
        help_text = "The link to the video of the day. Please enter the full link (e.g. 'https://www.google.com' instead of 'google.com').")
    visible_text = models.CharField(max_length = 500,
        help_text = "The front page text that will contain the video link.")
    description = models.CharField(blank = True, null = True, max_length = 1000,
        help_text = "A description of the video (optional).")
    time = models.DateTimeField(
        help_text = "The time and date the video will be shown.")

    class Meta:
        ordering = ['-time']

    def __str__(self):
        """String for representing the Model object."""
        return self.visible_text

class GameOfWeek(models.Model):
    """Model to display selected games under the `Games` tab."""
    game = models.CharField(max_length = 100,
        help_text = "The name of the game of the week (max 100 characters).")
    image = models.ImageField(
        help_text = "The image of the game of the week (most file formats work, please try to keep the file small).")
    time = models.DateTimeField(
        help_text = "The time and date the game will be shown.")

    class Meta:
        """Ordering of the Model objects."""
        ordering = ['-time']

    def __str__(self):
        """String for representing the Model object."""
        return self.game

class EmailAddress(models.Model):
    """Model to store email addresses of members."""
    email = models.EmailField(unique = True,
        help_text = "The email address of a Game Night member.");
    name = models.CharField(max_length = 200,
        help_text = "The name attached to the email address.");

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.email}'

# sources:
# https://stackoverflow.com/questions/42421366/delete-image-in-django
# https://stackoverflow.com/questions/13857007/using-pre-delete-signal-in-django
@receiver(post_delete, sender = GameOfWeek, dispatch_uid=  'game_of_week_delete_signal')
def delete_image_file(sender, instance, using, **kwargs):
    # You have to prepare what you need before deleting the model
    storage, path = instance.image.storage, instance.image.path
    # Delete the file after the model
    storage.delete(path)
