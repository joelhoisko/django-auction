from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# TODO make proper models
class Auction(models.Model):
    title = models.CharField(max_length=50, default='Auction Title')
    description = models.CharField(max_length=5000, default='')
    minimum_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    timestamp = models.DateTimeField('date published', default=0)
    deadline = models.DateTimeField('deadline', default=0)
    seller = models.ForeignKey(User)


# Used for connecting the creator of the Auction
# to the User. You shouldn't directly extend Djangos User-model
# so this table serves as a relationship for seller-auction.
# is this needed?
#class Seller(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    auction = models.ForeignKey(Auction)


