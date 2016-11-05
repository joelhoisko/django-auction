from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader


# Create your views here.


# default page
def index(request):
    # Check if we have a user logged in and display them a message
    if request.user.is_authenticated():
        context = {
            'welcome_text': 'Good day {}'.format(request.user.username)
        }
    else:
        context = {
            'welcome_text': 'Welcome!'
        }
    # Put the context with the HTML
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def check_login(request):
    # Get the users data
    username = request.POST['login_name']
    password = request.POST['login_password']
    # try to authenticate
    print('Authenticating...')
    user = authenticate(username=username, password=password)
    if user is not None:
        print('found the user, logging in!')
        # log the user in
        auth.login(request, user)
        # return back to the index page
        response = HttpResponseRedirect('/')
        return response
    else:
        # no user found, error!
        print('Invalid login!')
        return HttpResponse('Invalid login!')


# returns the registration page
def register_page(request):
    return render(request, 'register.html')


def add_user(request):
    # Get the users data from the form
    user_username = request.POST.get('Username')
    user_email = request.POST.get('Email')
    user_password = request.POST.get('Password')
    # Create the user from the data
    new_user = User.objects.create_user(username=user_username, email=user_email, password=user_password)
    new_user.save()
    # log in the new user immediately
    auth.login(request, new_user)
    # make the response redirect back to the index page
    response = HttpResponseRedirect('/')
    return response


def logout_view(request):
    auth.logout(request)
    response = HttpResponseRedirect('/')
    return response
