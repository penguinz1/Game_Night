from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class User(AbstractUser):
    """User model for the application."""
    pass


class GameScore(models.Model):
    score  = models.PositiveIntegerField()
    time   = models.DateTimeField(auto_now_add = True)
    player = models.ForeignKey('User', on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        """String for representing the Model object."""
        if (player):
            return f'{player.username} - {score}'
        else:
            return f'anonymous - {score}'


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
        if (person):
            return f'{person} - {game}'
        else:
            return f'anonymous - {game}'


class Meeting(models.Model):
    time     = models.DateTimeField()
    name     = models.CharField(max_length = 100, blank = True, null = True)
    location = models.ForeignKey('Location', on_delete = models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        if (name):
            return f'{name} - {time}'
        else:
            return time


class Location(models.Model):
    place = models.CharField(max_length = 200)

    def __str__(self):
        """String fo representing the Model object."""
        return place


class Contact(models.Model):
    message = models.CharField(max_length = 500)
    email   = models.EmailField(blank = True, null = True, max_length = 254, verbose_name='email address')

    def __str__(self):
        return message


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
        return f'{choice} - {new_email}'