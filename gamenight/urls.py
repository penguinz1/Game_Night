"""gamenight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls), # urls for the admin site
    path('', include('main.urls')), # all-purpose urls for the main site
    path('accounts/', include('accounts.urls')), # urls for User interfaces (sign-up, profile, etc.)
    path('accounts/', include('django.contrib.auth.urls')), # official django urls for User interfaces
    path('summernote/', include('django_summernote.urls')), # necessary for rich text input boxes
]

handler404 = 'main.views.handler404'