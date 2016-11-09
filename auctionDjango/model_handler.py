from auctionDjango import models
from django.utils import timezone
from django.core.mail import send_mail
import datetime
import pytz

# TODO create a method to send email to all people related to an Auction


# returns a list of all the Users who have taken some part in the Auction
def get_auction_bidders(auction):
    # initiate the list with the seller
    bidder_list = []
    # get all the bids of this particular Auction and iterate it
    # this has no duplicates, as we always remove a users old bids before bidding a new
    bids = models.Bid.objects.filter(auction=auction)
    for bid in bids:
        # add all the buyers to the people_list
        bidder_list.append(bid.buyer)
    # return the populated list
    return bidder_list


# check if the auction is due
def check_due(auction):
    # get the difference of the timedelta in seconds
    remaining_time = (auction.deadline - timezone.now()).total_seconds()
    # is it still valid?
    if remaining_time <= 0:
        # the auction is due! set that the auction is due
        auction.status = auction.STATUS_CHOICE[2][0]
        auction.save()
        # return true that the auction is indeed due
        return True
    # else, return False
    return False


# ends an Auctions cycle
def resolve_auction(auction):
    # send email to all the people
    send_mail(
        'Your auction {} is over!'.format(auction.item.title),
        'Your auction has ended!',
        'auctions@django_joel.com',
        [auction.seller.email],
        fail_silently=False,
    )
    # get the bidders
    bidder_list = get_auction_bidders(auction)
    # iterate through them
    for bidder in bidder_list:
        # the winner get's special mail
        if bidder == auction.winning_bid.buyer:
            send_mail(
                'You won {}!'.format(auction.item.title),
                'The auction for {} has ended, you won! Email the winner @{}'.format(auction.item.title, auction.seller.email),
                'auctions@django_joel.com',
                [bidder.email],
                fail_silently=False,
            )
        # boring mail for others
        else:
            send_mail(
                'An auction you have bid on has ended',
                'The auction for {} has ended, better luck next time!'.format(auction.item.title),
                'auctions@django_joel.com',
                [bidder.email],
                fail_silently=False,
            )
    # and make the auction 'Adjudicated'
    auction.status = auction.STATUS_CHOICE[3][0]
    auction.save()
    # the auction has officially closed!


# saves a new bid
def save_bid(form_data, auction, user):
    # first, remove your old bids about this same auction, if possible
    models.Bid.objects.filter(auction=auction, buyer=user).delete()

    # get the bid and create it
    bid_amount = form_data['bid_amount']
    new_bid = models.Bid(auction=auction, buyer=user, bid_amount=bid_amount)
    new_bid.save()

    # send email to the old winning bidder
    if auction.winning_bid is not None:
        send_mail(
            'Your bid on {} has been overtaken'.format(auction.item.title),
            'Your old bid has been overtaken!',
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
        'You bid on {}!'.format(auction.item.title),
        'You have created a bid!',
        'auctions@django_joel.com',
        [new_bid.buyer.email],
        fail_silently=False,
    )
    # and the seller
    send_mail(
        'A new bid on your item {}!'.format(auction.item.title),
        'A new bid has appeared on your auction!',
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
