from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.views import View
from auctionDjango import forms
from auctionDjango import model_handler
from auctionDjango.models import *


# Create your views here.

# the homepage
def home(request):
    return render(request, 'home.html')


# trying out some class-based views
# have to use a special method_decorator with 'dispatch' when dealing with classes
@method_decorator(login_required, name='dispatch')
class ProfileView(View):

    def get(self, request):
        # get the active Auctions where the user is the seller
        auctions = Auction.objects.filter(seller=request.user, status='AC')
        return render(request, 'profile.html', {'auctions': auctions})


# class for editing email
@method_decorator(login_required, name='dispatch')
class EditEmailView(View):
    # class attribute
    email_form = forms.EditEmail

    # return this for a POST-request, we could also use form_valid for extra fancy
    def post(self, request):
        # initialize a form and populate it
        form = self.email_form(request.POST)
        if form.is_valid():
            # save the information
            model_handler.save_email(form.cleaned_data, request.user)
            messages.add_message(request, messages.INFO, 'Email changed successfully!')
            return HttpResponseRedirect('/profile/')
        else:
            # add an extra error message
            messages.add_message(request, messages.ERROR, 'Please check the emails.')
            # return back to the form
            return self.get(request)

    # return this for a GET-request
    def get(self, request):
        return render(request, 'email.html', {'form': self.email_form})


@method_decorator(login_required, name='dispatch')
class EditPasswordView(View):
    password_form = forms.EditPassword

    def post(self, request):
        form = self.password_form(request.POST)
        if form.is_valid():
            # save the new password
            model_handler.save_password(form.cleaned_data, request.user)
            # authenticate the user again so that they are still logged in
            # also use form.user as request.user probably logs out immediately
            update_session_auth_hash(request, request.user)
            messages.add_message(request, messages.INFO, 'Password changed successfully!')
            return HttpResponseRedirect('/profile/')
        else:
            messages.add_message(request, messages.ERROR, 'Please check the passwords.')
            return self.get(request)

    def get(self, request):
        return render(request, 'password.html', {'form': self.password_form})


# for viewing an auction and bidding to it it
class AuctionView(View):
    # create some attributes
    auction = None
    bid_form = forms.BidForm

    def post(self, request, auction_id):
        # check the auction first
        try:
            self.auction = Auction.objects.get(id=auction_id)
        except ObjectDoesNotExist:
            raise Http404
        # create a copy of the form, this is all very, very tiring
        form = self.bid_form(request.POST)
        form.auction = self.auction
        form.buyer = request.user
        # check validity
        if form.is_valid():
            # save the new bid
            model_handler.save_bid(form.cleaned_data, self.auction, request.user)
            # get a nice message
            messages.add_message(request, messages.INFO, 'Your bid has been saved!')
            # return to the auctions page, remember to pass the auction_id
            return self.get(request, auction_id)
        else:
            messages.add_message(request, messages.ERROR, 'Invalid bid!')
            # save the form with errors to our classes form so that we can show the errors
            self.bid_form = form
            return self.get(request, auction_id)

    # get's the url-parameter(really badly documented in Django imo)
    def get(self, request, auction_id):
        try:
            # get the auction id and update the auction
            self.auction = Auction.objects.get(id=auction_id)
            # check that the auction is active, just in case the user directly inputs the url
            if self.auction.status != 'AC':
                raise Http404
            # format the context and add the form to it
            context = model_handler.format_auction(self.auction)
            # set the forms attributes, we could use the __init__ but im done with this
            self.bid_form.auction = self.auction
            self.bid_form.buyer = request.user
            context.update({'form': self.bid_form})
            return render(request, 'auction.html', context)
        except ObjectDoesNotExist:
            raise Http404


# for browsing all the Auctions
def browse(request):
    auctions = Auction.objects.filter(status='AC')
    return render(request, 'browse_auctions.html', {'auctions': auctions})


@login_required
def create_auction(request):
    if request.method == 'POST':
        # create a new instance and populate it
        auction_form = forms.CreateAuction(request.POST)
        # check validity
        if auction_form.is_valid():
            # get all the data and save them to variables
            data = auction_form.cleaned_data
            item_title = data['title']
            item_description = data['description']
            auction_minimum_price = data['minimum_price']
            auction_deadline = data['deadline'].timestamp()
            # create the confirmation form
            confirmation_form = forms.ConfirmAuction()
            # pass all the information into the context
            context = {
                'form': confirmation_form,
                'item_title': item_title,
                'item_description': item_description,
                'auction_minimum_price': auction_minimum_price,
                'auction_deadline': auction_deadline
            }
            # add a lil message and put the context into the site
            messages.add_message(request, messages.INFO, 'Are you sure that you want to create an auction?')
            return render(request, 'confirm_auction.html', context)
        else:
            messages.add_message(request, messages.ERROR, 'Please create a valid auction!')
    else:
        # create a blank form
        auction_form = forms.CreateAuction()

    return render(request, 'create_auction.html', {'form': auction_form})


@method_decorator(login_required, name='dispatch')
class AuctionEditView(View):
    edit_form = forms.DescriptionForm
    auction = None

    def post(self, request, auction_id):
        # get the form from POST
        form = self.edit_form(request.POST)
        if form.is_valid():
            # save the new description
            try:
                # get the auction
                self.auction = Auction.objects.get(id=auction_id)
            except ObjectDoesNotExist:
                raise Http404
            # save the form, add a message and redirect to /profile/
            model_handler.save_description(form.cleaned_data, self.auction)
            messages.add_message(request, messages.INFO, 'The description has been saved.')
            return HttpResponseRedirect('/profile/')
        else:
            messages.add_message(request, messages.ERROR, 'Description too long!')
            self.edit_form = form
            return self.get(request, auction_id)

    def get(self, request, auction_id):
        try:
            # get the auction
            self.auction = Auction.objects.get(id=auction_id)
        except ObjectDoesNotExist:
            raise Http404
        # check that the auction is active, just in case the user directly inputs the url
        if self.auction.status != 'AC':
            raise Http404
        # now make the description
        description = self.auction.item.description
        self.edit_form = forms.DescriptionForm(initial={'description': description})
        return render(request, 'edit_auction.html', {'form': self.edit_form})


# super dumb view, but bans a single auction
@method_decorator(staff_member_required, name='dispatch')
class AuctionBanView(View):

    def get(self, request, auction_id):
        try:
            auction = Auction.objects.get(id=auction_id)
        except ObjectDoesNotExist:
            raise Http404
        # ban the auction and return to the homepage
        model_handler.ban_auction(auction)
        return HttpResponseRedirect('/home/')


@login_required
def confirm_auction(request):
    # get the users answer and act accordingly
    answer = request.POST.get('answer')
    if answer == 'Yes':
        # send the data to model_handler to take care of it, cleaner that way
        model_handler.save_auction(request.POST, request.user)
        messages.add_message(request, messages.INFO, 'New auction created!')
        # send an email to the user, check settings.py for credentials
        send_mail(
            'You have created an auction!',
            'Congratulations!',
            'auctions@django_joel.com',
            [request.user.email],
            fail_silently=False,
        )

    # return to the homepage either way
    return HttpResponseRedirect('/')


# login view
def login(request):
    # check if we are coming here from the form
    if request.method == 'POST':
        # create an instance of the form and populate it with the one from the request
        login_form = forms.LoginUser(request.POST)
        # check the form
        if login_form.is_valid():
            data = login_form.cleaned_data
            username = data['username']
            password = data['password']
            # try to authenticate the user
            user = authenticate(username=username, password=password)
            # check that we are successful
            if user is not None and user.is_active:
                # log the user in and return to homepage
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.ERROR, 'That user doesn\'t exist!')

    # else, return the user with a blank login page
    else:
        login_form = forms.LoginUser()
    return render(request, 'login.html', {'form':login_form})


# register view
def register(request):
    if request.method == 'POST':
        # create a form and populate it with the user-filled form
        register_form = forms.RegisterUser(request.POST)
        # check the form
        if register_form.is_valid():
            # the form is good, get the clean data
            data = register_form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password']
            # create thee new user, save them and log them in
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            auth.login(request, new_user)
            # redirect
            return HttpResponseRedirect('/')
        else:
            # Add an error message if there is something wrong.
            messages.add_message(request, messages.ERROR, 'Not valid registration!')

    # If here for the first time, just give them the form.
    register_form = forms.RegisterUser()
    return render(request, 'register.html', {'form': register_form})


# logout the user
def logout_view(request):
    auth.logout(request)
    response = HttpResponseRedirect('/')
    return response
