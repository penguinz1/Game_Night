from django.contrib import admin
from django import forms
from django.db import models
from django_summernote.widgets import SummernoteWidget

from main.models import GameScore, Meeting, Location, EmailAddress, Contact, MassEmail, ContactNotificant
from main.models import Alert, GameBring, QuoteOfDay, VideoOfDay, GameOfWeek

# Register your models here.

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ('score', 'drifters', 'time', 'player')
    list_filter = ('time',)

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('time', 'name', 'location')
    list_filter = ('location',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('place', 'latitude', 'longitude')

@admin.register(EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('message', 'email', 'time', 'seen')
    list_filter = ('seen', 'time')
    formfield_overrides = {
        models.CharField: {'widget': forms.Textarea(attrs = {'cols': 80, 'rows': 20})}
    }

class MassEmailAdminForm(forms.ModelForm):
    class Meta:
        model = MassEmail
        fields = '__all__'
        widgets = {
            'subject': forms.TextInput(attrs = {'size': 80}),
            'content': SummernoteWidget()
        }

@admin.register(MassEmail)
class MassEmailAdmin(admin.ModelAdmin):
    form = MassEmailAdminForm
    list_display = ('subject', 'last_edit', 'editor', 'is_sent')
    list_filter = ('is_sent',)

@admin.register(ContactNotificant)
class ContactNotificantAdmin(admin.ModelAdmin):
    list_display = ('email',)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('message', 'time', 'severity')
    list_filter = ('severity', 'time')
    formfield_overrides = {
        models.CharField: {'widget': forms.Textarea(attrs = {'cols': 80, 'rows': 20})}
    }

@admin.register(GameBring)
class GameBringAdmin(admin.ModelAdmin):
    list_display = ('game', 'person', 'meeting')
    list_filter = ('game',)


class QuoteOfDayForm(forms.ModelForm):
    class Meta:
        model = QuoteOfDay
        fields = '__all__'
        widgets = {
            'quote': forms.Textarea(attrs = {'cols': 100, 'rows': 5})
        }

@admin.register(QuoteOfDay)
class QuoteOfDayAdmin(admin.ModelAdmin):
    form = QuoteOfDayForm
    list_display = ('quote', 'speaker', 'time')
    list_filter = ('time',)

@admin.register(VideoOfDay)
class VideoOfDayAdmin(admin.ModelAdmin):
    list_display = ('visible_text', 'description', 'time')
    list_filter = ('time',)

@admin.register(GameOfWeek)
class GameOfWeekAdmin(admin.ModelAdmin):
    list_display = ('game', 'time')

admin.site.site_header = 'Game Night Website Administration'
admin.site.site_title = 'Game Night'
admin.site.index_title = "Website Admin"