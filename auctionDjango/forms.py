from django import forms
from django.utils import timezone
import datetime
from auctionDjango.auction_validators import *


class RegisterUser(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class LoginUser(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateAuction(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    minimum_price = forms.DecimalField()
    deadline = forms.DateTimeField(initial=timezone.now(), validators=[validate_deadline], help_text='Format should be ')

