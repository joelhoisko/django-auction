from django.core.management.base import BaseCommand, CommandError
from auctionDjango.models import Auction
from auctionDjango import model_handler


class Command(BaseCommand):
    help = 'goes through all the auctions, ' \
           'checks if they are due and resolves them'

    def handle(self, *args, **options):
        # get all the active auctions
        try:
            ac_auctions = Auction.objects.filter(status='AC')
        except Auction.DoesNotExist:
            raise CommandError('No active auctions going on!')

        for auction in ac_auctions:
            if model_handler.check_due(auction):
                # the auction was due, now resolve it
                model_handler.resolve_auction(auction)
        # write about the success
        self.stdout.write(self.style.SUCCESS('Auctions checked!'))