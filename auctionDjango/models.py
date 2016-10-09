from django.db import models

# Create your models here.


class User(models.Model):
    # Maybe tinker with the max_length values?
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=100)


# TODO make proper models
class Auction(models.Model):

    timestamp = models.DateTimeField('date published')
