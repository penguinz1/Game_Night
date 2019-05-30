from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class User(AbstractUser):
    """User model for the application."""
    pass


class GameScore(models.Model):
    score    = models.PositiveIntegerField()
    drifters = models.PositiveIntegerField()
    time     = models.DateTimeField(auto_now_add = True)
    player   = models.ForeignKey('User', on_delete = models.SET_NULL, blank = True, null = True)

    def __str__(self):
        """String for representing the Model object."""
        if (self.player):
            return f'{self.player.username} - {self.score}'
        else:
            return f'anonymous - {self.score}'


class Alert(models.Model):
    MESSAGE = '1m'
    ALERT   = '2a'
    WARNING = '3w'
    SEVERITY_CHOICES = (
        (MESSAGE, 'Message'),
        (ALERT, 'Alert'),
        (WARNING, 'Warning'),
    )

    message  = models.CharField(max_length = 250)
    time     = models.DateTimeField()
    seen     = models.ManyToManyField('User', blank = True)
    severity = models.CharField(max_length = 2, choices = SEVERITY_CHOICES)

    class Meta:
        ordering = ['-severity', 'time']

    def __str__(self):
        """String for representing the Model object."""
        return self.message


class GameBring(models.Model):
    game    = models.CharField(max_length = 100)
    person  = models.CharField(max_length = 180, blank = True, null = True)
    meeting = models.ForeignKey('Meeting', on_delete = models.CASCADE)

    class Meta:
        ordering = ['game']

    def __str__(self):
        """String for representing the Model object."""
        if (self.person):
            return f'{self.person} - {self.game}'
        else:
            return f'anonymous - {self.game}'


class Meeting(models.Model):
    time     = models.DateTimeField()
    name     = models.CharField(max_length = 100, blank = True, null = True)
    location = models.ForeignKey('Location', on_delete = models.CASCADE)
    email    = models.OneToOneField('MassEmail', on_delete = models.SET_NULL, blank = True, null = True)

    class Meta:
        ordering = ['time']

    def __str__(self):
        """String for representing the Model object."""
        if (self.name):
            return f'{self.name} - {self.time}'
        else:
            return f'{self.time}'

class MassEmail(models.Model):
    subject   = models.CharField(max_length = 200)
    content   = models.CharField(max_length = 1000)
    last_edit = models.DateTimeField(auto_now_add = True)
    editor    = models.ForeignKey('User', on_delete = models.SET_NULL, blank = True, null = True)
    is_sent   = models.BooleanField(default = False)

    class Meta:
        permissions = (('can_send_emails', 'Abilty to send club emails'),)

    def __str__(self):
        """String for representing the Model object."""
        return self.subject;


class Location(models.Model):
    place = models.CharField(max_length = 200)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])

    def __str__(self):
        """String fo representing the Model object."""
        return self.place


class Contact(models.Model):
    message = models.CharField(max_length = 500)
    email   = models.EmailField(blank = True, null = True, max_length = 254, verbose_name='email address')
    seen    = models.BooleanField(default = False)

    def __str__(self):
        return self.message

class ContactNotificant(models.Model):
    email = models.EmailField()

    def __str__(self):
        return f'{self.email}'

class QuoteOfDay(models.Model):
    quote = models.CharField(max_length = 500)
    speaker = models.CharField(max_length = 200)
    time = models.DateTimeField()

    class meta:
        ordering = ['-time']

    def __str__(self):
        return f'{self.speaker} - {self.quote}'

class VideoOfDay(models.Model):
    link = models.CharField(max_length = 1000)
    visible_text = models.CharField(max_length = 500)
    description = models.CharField(blank = True, null = True, max_length = 1000)
    time = models.DateTimeField()

    class meta:
        ordering = ['-time']

    def __str__(self):
        return self.visible_text

class GameOfWeek(models.Model):
    game = models.CharField(max_length = 100)
    image = models.ImageField()
    time = models.DateTimeField()

    class meta:
        ordering = ['-time']

    def __str__(self):
        return self.game

class EmailAddress(models.Model):
    email = models.EmailField(unique = True);
    name = models.CharField(max_length = 200);

    def __str__(self):
        return f'{self.email}'
