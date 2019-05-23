from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label = "Email", required = False)
    first_name = forms.CharField(label = "First Name", required = False)
    last_name = forms.CharField(label = "Last Name", required = False)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

    UserCreationForm.Meta.model = User


class ProfileChangeForm(forms.Form):
    email = forms.EmailField(label = "Email", required = False)
    first_name = forms.CharField(label = "First Name", required = False)
    last_name = forms.CharField(label = "Last Name", required = False)