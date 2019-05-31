from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE

from main.models import Contact, EmailAddress

class CreateContactForm(ModelForm):
    """Form to create a Contact model object."""
    message = forms.CharField(max_length = 500, 
        widget = forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    email = forms.EmailField(required = False)

    class Meta:
        model = Contact
        fields = ['message', 'email']

class MassEmailForm(forms.Form):
    """Form to create a mass email to send."""
    subject = forms.CharField(max_length = 200)
    content = forms.CharField(max_length = 1000, widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

class TestEmailForm(forms.Form):
    """Form to send a test email."""
    recipient = forms.EmailField()

class AddMailForm(forms.Form):
    """Form to add an email address to the database."""
    new_mail = forms.EmailField();
    name     = forms.CharField(max_length = 200);

    # verify email is not already inside the database
    def clean_new_mail(self):
        new_mail = self.cleaned_data['new_mail']
        if (EmailAddress.objects.filter(email = new_mail).exists()):
            raise ValidationError(_("Email already exists"))
        return new_mail

class ModifyMailForm(forms.Form):
    """Form to move an email address within the database."""
    old_mail = forms.EmailField();
    new_mail = forms.EmailField();

    # verify old email is in the database
    def clean_old_mail(self):
        old_mail = self.cleaned_data['old_mail']
        if (not EmailAddress.objects.filter(email = old_mail).exists()):
            raise ValidationError(_("Old email doesn't exist"))
        return old_mail

    # verify new email is not already inside the database
    def clean_new_mail(self):
        new_mail = self.cleaned_data['new_mail']
        if (EmailAddress.objects.filter(email = new_mail).exists()):
            raise ValidationError(_("New email already exists"))
        return new_mail

class DeleteMailForm(forms.Form):
    """Form to delete an email address from the database."""
    delete_mail = forms.EmailField();

    # verify email is in the database
    def clean_old_mail(self):
        delete_mail = self.cleaned_data['delete_mail']
        if (not EmailAddress.objects.filter(email = delete_mail).exists()):
            raise ValidationError(_("Email doesn't exist"))
        return delete_mail

class GameBringForm(forms.Form):
    """Form for creating a GameBring model object."""
    game   = forms.CharField(max_length = 100)
    person = forms.CharField(max_length = 180, required = False)
    