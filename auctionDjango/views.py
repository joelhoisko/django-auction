from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from auctionDjango import forms
from auctionDjango.models import Auction

# Create your views here.


# the homepage
def home(request):
    return render(request, 'home.html')


@login_required
def create_auction(request):
    if request.method == 'POST':
        # create a new instance and populate it
        auction_form = forms.CreateAuction(request.POST)
        # check validity
        print(auction_form.errors)
        if auction_form.is_valid():
            data = auction_form.cleaned_data
            title = data['title']
            description = data['description']
            minimum_price = data['minimum_price']
            timestamp = timezone.now()
            deadline = data['deadline']

            # create a new auction
            new_auction = Auction(title=title, description=description, minimum_price=minimum_price,
                                  timestamp=timestamp, deadline=deadline, seller=request.user)
            new_auction.save()

            messages.add_message(request, messages.INFO, 'A new auction has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Please create a valid auction!')

    auction_form = forms.CreateAuction()
    return render(request, 'create_auction.html', {'form': auction_form})


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

    # If here for the first time, just give them te form.
    register_form = forms.RegisterUser()
    return render(request, 'register.html', {'form': register_form})


# logout the user
def logout_view(request):
    auth.logout(request)
    response = HttpResponseRedirect('/')
    return response
