from auctionDjango import models
from django.utils import timezone
from django.core.mail import send_mail
import datetime
import pytz

# TODO create a method to send email to all people related to an Auction


# saves a new bid
def save_bid(form_data, auction, user):
    # get the bid and create it
    bid_amount = form_data['bid_amount']
    new_bid = models.Bid(auction=auction, buyer=user, bid_amount=bid_amount)
    new_bid.save()

    # send email to the old winning bidder
    if auction.winning_bid is not None:
        send_mail(
            'A new bid!',
            'A new bid has appeared on an auction you have bid on!',
            'auctions@django_joel.com',
            [auction.winning_bid.buyer.email],
            fail_silently=False,
        )
    # then save the new bid to the Auction
    # don't forget to save it to the Auction too (not that I've done it)
    auction.winning_bid = new_bid
    auction.save()
    # then email the new bidder
    send_mail(
        'A new bid!',
        'A new bid has appeared on an auction you have bid on!',
        'auctions@django_joel.com',
        [new_bid.buyer.email],
        fail_silently=False,
    )
    # and the seller
    send_mail(
        'A new bid!',
        'A new bid has appeared on an auction you have bid on!',
        'auctions@django_joel.com',
        [auction.seller.email],
        fail_silently=False,
    )


# pulls the information from the dictionary and creates a new item-auction
def save_auction(dictionary, user):
    # create and save the item
    title = dictionary['item_title']
    description = dictionary['item_description']
    new_item = models.Item(title=title, description=description)
    new_item.save()
    # create the auction and save it
    minimum_price = dictionary['auction_minimum_price']
    # have to convert it to float
    deadline = float(dictionary['auction_deadline'])
    # get the time from the stamp
    deadline = datetime.datetime.fromtimestamp(deadline)
    # make the time aware
    deadline = pytz.utc.localize(deadline)
    timestamp = timezone.now()
    new_auction = models.Auction(item=new_item, minimum_price=minimum_price, timestamp=timestamp,
                                 deadline=deadline, seller=user)
    new_auction.save()


# formats the auctions date string mostly, I could do inside the Auction -class...
def format_auction(auction):
    until_deadline = auction.deadline - timezone.now()
    days_left = until_deadline.days
    hours_left = until_deadline.seconds // 3600
    minutes_left = until_deadline.seconds % 3600 // 60
    return {
        'auction': auction,
        'days': days_left,
        'hours': hours_left,
        'minutes': minutes_left
    }


# saves the email address to the user
def save_email(form_data, user):
    confirm_new_email = form_data['confirm_new_email']
    user.email = confirm_new_email
    user.save()


# saves the users new password
def save_password(form_data, user):
    new_password = form_data['confirm_new_password']
    user.set_password(new_password)
    user.save()
