from django import forms

from .models import Event


class NewEventForm(forms.Form):
    name = forms.CharField(label='Event Name', max_length=50)
    date = forms.DateField(label='Date', widget=forms.DateTimeInput())


class NewParticipantForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    auth_code = forms.CharField(label='Auth Code', max_length=4)


class AuthCodeForm(forms.Form):
    auth_code = forms.CharField(label='Auth Code', max_length=4)
