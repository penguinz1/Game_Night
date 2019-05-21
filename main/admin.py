from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import GameScore, Meeting, Location, EmailAddress, Contact, MassEmail

from .models import User
# Register your models here.
admin.site.register(User, UserAdmin)

admin.site.register(GameScore)
admin.site.register(Meeting)
admin.site.register(Location)
admin.site.register(EmailAddress)
admin.site.register(Contact)
admin.site.register(MassEmail)