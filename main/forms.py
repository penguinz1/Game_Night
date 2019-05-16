from django import forms
from django.forms import ModelForm
from tinymce.widgets import TinyMCE

from main.models import Contact

class CreateContactForm(ModelForm):
    message = forms.CharField(max_length = 500, 
        widget = forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    class Meta:
        model = Contact
        fields = {'message', 'email'}


class MassEmailForm(forms.Form):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

class AddMailForm(forms.Form):
    new_mail = forms.EmailField();

class ModifyMailForm(forms.Form):
    old_mail = forms.EmailField();
    new_mail = forms.EmailField();

class DeleteMailForm(forms.Form):
    delete_mail = forms.EmailField();
