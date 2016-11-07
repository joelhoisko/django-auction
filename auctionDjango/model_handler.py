from auctionDjango import models
from django.utils import timezone
import datetime
import pytz

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
                                 deadline=deadline, current_price=minimum_price, seller=user)
    new_auction.save()
