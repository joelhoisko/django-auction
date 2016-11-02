from django.db import models

# Create your models here.


# TODO make proper models
class Auction(models.Model):

    timestamp = models.DateTimeField('date published')
