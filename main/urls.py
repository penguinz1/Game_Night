from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name = 'index'),
    path('alert', views.alert_update, name = 'alert'),
    path('contact', views.contact, name = 'contact'),
    path('mass-mail', views.mass_mail, name = 'mass_mail'),
    path('mass-mail-submit', views.mass_mail_submit, name = 'mass_mail_submit'),
    path('mass-mail-test', views.mass_mail_test, name = 'mass_mail_test'),
    path('email-list-index', views.email_list_index, name = 'email_list_index'),
    path('time-and-location', views.time_location, name = 'time_location'),
    path('email-list-add', views.add_email, name = 'add_email'),
    path('email-list-modify', views.modify_email, name = 'modify_email'),
    path('email-list-delete', views.delete_email, name = 'delete_email'),
    path('random', views.random, name = 'random'),
    path('space-game', views.space_game, name = 'space_game'),
    path('experimental', views.experimental, name = 'experimental'),
    path('games', views.games, name = 'games'),
    path('games-form', views.game_bring, name = 'game_bring'),
    path('changelog', TemplateView.as_view(template_name = "changelog.html"), name = 'changelog'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)