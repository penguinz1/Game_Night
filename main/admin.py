from django.contrib import admin

from main.models import GameScore, Meeting, Location, EmailAddress, Contact, MassEmail, ContactNotificant
from main.models import Alert, GameBring, QuoteOfDay, VideoOfDay, GameOfWeek

# Register your models here.
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

admin.site.site_header = 'Game Night Website Administration'
admin.site.site_title = 'Game Night'
admin.site.index_title = "Website Admin"