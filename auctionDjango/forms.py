from django import forms
from auctionDjango.auction_validators import *


# form to register users with
class RegisterUser(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


# form to login with
class LoginUser(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# form to create a new auction with
class CreateAuction(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    minimum_price = forms.DecimalField()
    deadline = forms.DateTimeField(initial=timezone.now(), validators=[validate_deadline],
                                   help_text='Format should be "YYYY-MM-DD HH:MM:SS"')


class ConfirmAuction(forms.Form):
    CHOICES = (('Yes', 'Yes'), ('No', 'No'))
    answer = forms.ChoiceField(choices=CHOICES)
