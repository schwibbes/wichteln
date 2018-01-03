from django import forms

from .models import Event


class NewEventForm(forms.Form):
    name = forms.CharField(label='Name des Events', max_length=50)
    admin_name = forms.CharField(label='Name des Organisators', max_length=50)
    date = forms.DateField(label='Date', widget=forms.DateTimeInput())
    description = forms.CharField(label='Beschreibung',widget= forms.Textarea, max_length=2000, required=False)

class NewParticipantForm(forms.Form):
    name = forms.CharField(label='Dein Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100, required=False)
    auth_code = forms.CharField(label='Auth Code', max_length=4)


class AuthCodeForm(forms.Form):
    auth_code = forms.CharField(label='Auth Code', max_length=4)
