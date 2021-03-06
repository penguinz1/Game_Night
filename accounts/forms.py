from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from accounts.models import User

class RegistrationForm(UserCreationForm):
    """Form to create a new account."""
    email = forms.EmailField(label = "Email", required = False,
        help_text = "Enter an email address (optional).")
    first_name = forms.CharField(label = "First Name", required = False,
        help_text = "Enter your first name (optional).")
    last_name = forms.CharField(label = "Last Name", required = False,
        help_text = "Enter your last name (optional).")
    if not settings.TEST_MODE:
        captcha = ReCaptchaField(widget = ReCaptchaV2Checkbox, label = "Verification")

    # saves form information into a User model object
    def save(self, commit = True):
        user = super(RegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

    UserCreationForm.Meta.model = User


class ProfileChangeForm(forms.Form):
    """Form to change User fields."""
    first_name = forms.CharField(label = "First Name", required = False,
        help_text = "Enter your first name (optional).")
    last_name = forms.CharField(label = "Last Name", required = False,
        help_text = "Enter your last name (optional).")
    email = forms.EmailField(label = "Email", required = False,
        help_text = "Enter an email address (optional).")