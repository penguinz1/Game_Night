from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import GameScore

from .models import User
# Register your models here.
admin.site.register(User, UserAdmin)

admin.site.register(GameScore)