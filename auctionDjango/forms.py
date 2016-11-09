from django import forms
from _decimal import *
from django.core.validators import MinValueValidator
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


class BidForm(forms.Form):
    bid_amount = forms.DecimalField(max_digits=9, decimal_places=2,
                                    validators=[MinValueValidator(Decimal('0.01'))])
    # these are set in the view, I kow it's ugly
    auction = None
    buyer = None

    # override the default clean
    def clean(self):
        # call for super so that we don't break the inherited clean()
        cleaned_data = super(BidForm, self).clean()
        # get the bid amount and the auction id
        bid_amount = cleaned_data.get('bid_amount')
        # get the auctions current price
        if self.auction.winning_bid is None:
            current_price = self.auction.minimum_price
        else:
            if self.buyer == self.auction.winning_bid.buyer:
                raise forms.ValidationError('You are already winning, can\'t bid again!')

            current_price = self.auction.winning_bid.bid_amount

        # check that the bid amount is valid
        if bid_amount is None:
            raise forms.ValidationError('Please use only 2 decimals.')
        # check that buyer != seller
        if self.buyer == self.auction.seller:
            raise forms.ValidationError('You can not bid on your own auction!')

        # now check that the bid is bigger by 0.01 at least
        # use Decimals for this, because floating point I guess
        if (Decimal(bid_amount) - Decimal(current_price)) < Decimal('0.01'):
            raise forms.ValidationError('Minimum bid increment is 0.01€!')

        return cleaned_data


# edit the users email
class EditEmail(forms.Form):
    new_email = forms.EmailField()
    confirm_new_email = forms.EmailField()

    # method for checking the emails
    # overrides the default clean()-method
    def clean(self):
        # call for super so that we don't break the inherited clean()
        cleaned_data = super(EditEmail, self).clean()
        # get the emails, have to use .get(), otherwise it might break it KeyError
        new_email = cleaned_data.get('new_email')
        confirm_new_email = cleaned_data.get('confirm_new_email')
        # check that there is a confirmation email
        if not confirm_new_email:
            raise forms.ValidationError('Confirm your new email!')
        # check that the emails match
        if new_email != confirm_new_email:
            raise forms.ValidationError('Your emails don not match!')

        return cleaned_data


class EditPassword(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput)

    # override the default clean so that we can do fancy form validating
    def clean(self):
        # call for super so the inherited stuff doesn't break
        cleaned_data = super(EditPassword, self).clean()
        # get the passwords, use get()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        # check that there is a confirmation
        if not confirm_new_password:
            raise forms.ValidationError('Please confirm your new password!')
        # check that they match
        if new_password != confirm_new_password:
            raise forms.ValidationError('Passwords do not match!')

        return cleaned_data


class DescriptionForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)


# form to create a new auction with
class CreateAuction(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    minimum_price = forms.DecimalField(validators=[MinValueValidator(Decimal('0.01'))])
    deadline = forms.DateTimeField(initial=timezone.now(), validators=[validate_deadline],
                                   help_text='Format should be "YYYY-MM-DD HH:MM:SS"')


class ConfirmAuction(forms.Form):
    CHOICES = (('Yes', 'Yes'), ('No', 'No'))
    answer = forms.ChoiceField(choices=CHOICES)
