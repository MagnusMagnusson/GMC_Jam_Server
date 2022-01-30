from django.core.management.base import BaseCommand, CommandError
import yoyocoin.roundReset as roundTwo


class Command(BaseCommand):
    help = 'Starts round 2 of the YoYoMarket'

    def handle(self, *args, **options):
        #Kill round 1
        roundTwo.burnDatabase()
        roundTwo.resetMoney()
        roundTwo.resetCompanyShares()
        #Init round 2
        roundTwo.populateNews()
        roundTwo.initSharePrice()
        #Let's go!
        roundTwo.open()