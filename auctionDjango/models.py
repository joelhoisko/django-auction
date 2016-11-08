from django.db import models
from django.contrib.auth.models import User
from auctionDjango.auction_validators import *
# Create your models here.


# represents a single, auctionable item
class Item(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)


# a single Auction-happening with prices and bidding etc
class Auction(models.Model):
    STATUS_CHOICE = (
        ('AC', 'Active'),
        ('BA', 'Banned'),
        ('DU', 'Due'),
        ('AD', 'Adjudicated'),
    )
    item = models.ForeignKey(Item)
    minimum_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    timestamp = models.DateTimeField('date published')
    deadline = models.DateTimeField('deadline', validators=[validate_deadline])
    # have to use 'Bid' to refer to model that has not yet been declared
    winning_bid = models.ForeignKey('Bid', null=True, related_name='auction_winner')
    seller = models.ForeignKey(User, related_name='seller')
    status = models.CharField(max_length=2, choices=STATUS_CHOICE, default=STATUS_CHOICE[0][0])


# represents a single bid to an auction
class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='auction_to_bid')
    buyer = models.ForeignKey(User)
    bid_amount = models.DecimalField(max_digits=9, decimal_places=2)

