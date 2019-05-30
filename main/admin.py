from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import GameScore, Meeting, Location, EmailAddress, Contact, MassEmail, ContactNotificant
from main.models import Alert, GameBring, QuoteOfDay, VideoOfDay, GameOfWeek

from .models import User
# Register your models here.
admin.site.register(User, UserAdmin)

admin.site.register(GameScore)
admin.site.register(Meeting)
admin.site.register(Location)
admin.site.register(EmailAddress)
admin.site.register(Contact)
admin.site.register(MassEmail)
admin.site.register(ContactNotificant)
admin.site.register(Alert)
admin.site.register(GameBring)
admin.site.register(QuoteOfDay)
admin.site.register(VideoOfDay)
admin.site.register(GameOfWeek)