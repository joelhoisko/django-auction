"""auction_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from auctionDjango import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', views.home, name='home'),
    url(r'^browse/$', views.BrowseView.as_view()),
    url(r'^auction/(?P<auction_id>\d+)/ban/', views.AuctionBanView.as_view()),
    url(r'^auction/(?P<auction_id>\d+)/', views.AuctionView.as_view()),
    url(r'^register/', views.register),
    url(r'^editauction/(?P<auction_id>\d+)/', views.AuctionEditView.as_view()),
    url(r'^create_auction/confirm/', views.confirm_auction),
    url(r'^create_auction/', views.create_auction),
    url(r'^profile/email/', views.EditEmailView.as_view()),
    url(r'^profile/password/', views.EditPasswordView.as_view()),
    url(r'^profile/', views.ProfileView.as_view()),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout_view),
    url(r'$', views.home)
]
