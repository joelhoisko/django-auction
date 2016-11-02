from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# default page
def index(request):
    # get the cookie
    if 'welcome_text' in request.COOKIES:
        context = {
            'welcome_text': request.COOKIES['welcome_text']
        }
    else:
        # if cookie not found, make a default
        context = {
            'welcome_text': 'Hello!'
        }

    # Load the cookie into the index.html and return it
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def check_login(request):
    # Get the users data
    username = request.POST['login_name']
    password = request.POST['login_password']
    # try to authenticate
    user = authenticate(username=username, password=password)
    if user is not None:
        welcome_text = 'Welcome back {}!'.format(username)
        response = HttpResponseRedirect('/')
        response.set_cookie('welcome_text', welcome_text)
        return response
    else:
        return HttpResponse('Invalid login!')


# returns registration page
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

    # make the welcome text
    welcome_text = 'Welcome {}'.format(user_username)
    # make the response redirect back to the index page and add the cookie to the response
    response = HttpResponseRedirect('/')
    response.set_cookie('welcome_text', welcome_text)
    return response

