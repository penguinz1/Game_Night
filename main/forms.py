from django import forms
from django.forms import ModelForm
from tinymce.widgets import TinyMCE

from main.models import Contact

class CreateContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = {'message', 'email'}


class MassEmailForm(forms.Form):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

