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
    message = models.CharField(max_length = 250)
    time    = models.DateTimeField()
    seen    = models.ManyToManyField('User')

    def __str__(self):
        """String for representing the Model object."""
        return message


class GameBring(models.Model):
    game    = models.CharField(max_length = 50)
    person  = models.CharField(max_length = 180, blank = True, null = True)
    meeting = models.ForeignKey('Meeting', on_delete = models.CASCADE)

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

    def __str__(self):
        """String for representing the Model object."""
        if (self.name):
            return f'{self.name} - {self.time}'
        else:
            return f'{self.time}'

class MassEmail(models.Model):
    subject = models.CharField(max_length = 200)
    content = models.CharField(max_length = 1000)

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

    def __str__(self):
        return self.message


class EmailRequest(models.Model):
    ADDITION     = 'a'
    MODIFICATION = 'm'
    DELETE       = 'd'
    EMAIL_CHOICES = (
        ('a', 'Add New'),
        ('m', 'Modify Existing'),
        ('d', 'Delete'),
    )

    new_email = models.EmailField(max_length = 254)
    old_email = models.EmailField(blank = True, null = True, max_length = 254)

    choice    = models.CharField(
        max_length = 1,
        choices = EMAIL_CHOICES,
        default = ADDITION,
    )

    def __str__(self):
        return f'{self.choice} - {self.new_email}'

class QuoteOfDay(models.Model):
    quote = models.CharField(max_length = 500)
    speaker = models.CharField(max_length = 200)
    time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.speaker} - {self.quote}'

class VideoOfDay(models.Model):
    link = models.CharField(max_length = 1000)
    description = models.CharField(max_length = 1000)
    visible_text = models.CharField(blank = True, null = True, max_length = 500)

    def __str__(self):
        return description

class EmailAddress(models.Model):
    email = models.EmailField(unique = True);
    name = models.CharField(max_length = 200);

    def __str__(self):
        return f'{self.email}'
