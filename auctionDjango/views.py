from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from auctionDjango import forms
from auctionDjango import model_handler
from auctionDjango.models import *


# Create your views here.


# the homepage
def home(request):
    return render(request, 'home.html')


def auction_view(request, auction_id):
    try:
        auction = Auction.objects.get(id=auction_id)
        until_deadline = auction.deadline - timezone.now()
        days_left = until_deadline.days
        hours_left = until_deadline.seconds // 3600
        minutes_left = until_deadline.seconds % 3600 // 60
        context = {
            'auction': auction,
            'days': days_left,
            'hours': hours_left,
            'minutes': minutes_left
        }
        return render(request, 'auction.html', context)
    except ObjectDoesNotExist:
        raise Http404


# for browsing all the Auctions
def browse(request):
    auctions = Auction.objects.all()
    return render(request, 'browse_auctions.html', {'auctions': auctions})


@login_required
def create_auction(request):
    if request.method == 'POST':
        # create a new instance and populate it
        auction_form = forms.CreateAuction(request.POST)
        # check validity
        print(auction_form.errors)
        if auction_form.is_valid():
            # get all the data and save them to variables
            data = auction_form.cleaned_data
            item_title = data['title']
            item_description = data['description']
            auction_minimum_price = data['minimum_price']
            auction_deadline = data['deadline'].timestamp()
            print('From the view, fresh from the form:')
            print(auction_deadline)
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


@login_required
def confirm_auction(request):
    # get the users answer and act accordingly
    answer = request.POST.get('answer')
    if answer == 'Yes':
        # send the data to model_handler to take care of it, cleaner that way
        model_handler.save_auction(request.POST.copy(), request.user)
        messages.add_message(request, messages.INFO, 'New auction created!')

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

    # If here for the first time, just give them te form.
    register_form = forms.RegisterUser()
    return render(request, 'register.html', {'form': register_form})


# logout the user
def logout_view(request):
    auth.logout(request)
    response = HttpResponseRedirect('/')
    return response
