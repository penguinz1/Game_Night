from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteWidget

from main.models import Contact, EmailAddress

class CreateContactForm(ModelForm):
    """Form to create a Contact model object."""
    message = forms.CharField(max_length = 500, 
        widget = forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        help_text = "Enter your message (max 500 characters).")
    email = forms.EmailField(required = False,
        help_text = "Enter your email address (optional). This is best used if you want us to contact you back.")

    class Meta:
        model = Contact
        fields = ['message', 'email']

class MassEmailForm(forms.Form):
    """Form to create a mass email to send."""
    subject = forms.CharField(max_length = 200,
        help_text = "Enter the subject line of the mass email (max 200 characters).")
    content = forms.CharField(max_length = 2000, widget = SummernoteWidget(),
        help_text = "Enter the content of the mass email.")

class TestEmailForm(forms.Form):
    """Form to send a test email."""
    recipient = forms.EmailField(
        help_text = "Enter an email address that will receive the mass email.")

class AddMailForm(forms.Form):
    """Form to add an email address to the database."""
    new_mail = forms.EmailField(
        help_text = "Enter a new email address to add to the mailing list.");
    name     = forms.CharField(max_length = 200,
        help_text = "Enter your name (first and last please).");

    # verify email is not already inside the database
    def clean_new_mail(self):
        new_mail = self.cleaned_data['new_mail']
        if (EmailAddress.objects.filter(email = new_mail).exists()):
            raise ValidationError(_("Email already exists"))
        return new_mail

class ModifyMailForm(forms.Form):
    """Form to move an email address within the database."""
    old_mail = forms.EmailField(
        help_text = "Enter an email address already on the mailing list where you no longer want to receive emails.");
    new_mail = forms.EmailField(
        help_text = "Enter a new email address that will replace the old email address on the mailing list.");

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
    delete_mail = forms.EmailField(
        help_text = "Enter an email address to be deleted from the mailing list.");

    # verify email is in the database
    def clean_delete_mail(self):
        delete_mail = self.cleaned_data['delete_mail']
        if (not EmailAddress.objects.filter(email = delete_mail).exists()):
            raise ValidationError(_("Email doesn't exist"))
        return delete_mail

class GameBringForm(forms.Form):
    """Form for creating a GameBring model object."""
    game   = forms.CharField(max_length = 100,
        help_text = "Enter a game that you will bring to the next meeting (max 100 characters).")
    person = forms.CharField(max_length = 180, required = False,
        help_text = "Enter your name (optional).")
    