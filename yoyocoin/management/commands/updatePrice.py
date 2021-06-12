from django.core.management.base import BaseCommand, CommandError
import random
import decimal
import datetime
from yoyocoin.models import Company, Value, Tweet

baseShares = 10000
startValue = 100

class Command(BaseCommand):
    help = 'Updates the YoYocoin base value'

    def handle(self, *args, **options):
        if datetime(2021, 6, 14, 9, 0, 0) < datetime.now():
            return False
        for comp in Company.objects.all():
            latest = comp.value_set.all().order_by("-time")
            
            r0 = decimal.Decimal(random.random()*random.random() * 2 - random.random()*random.random()*1.94)
            r1 = decimal.Decimal(random.randint(40,80))
            lc = latest[0]
            now = datetime.datetime.now()
            tweets = Tweet.objects.all().filter(time__lte = now).filter(time__gte = lc.time)
            vc = 0
            for tweet in tweets:
                vc += tweet.valueChange
            tv = lc.targetvalue + (vc)*decimal.Decimal(comp.mediaDrive)
            nextcoin = Value()
            basevalue = lc.basevalue + ((tv * decimal.Decimal(comp.shares/comp.baseshares) - lc.basevalue)/r1)
            nextcoin.basevalue = basevalue
            nextcoin.value = max(1, basevalue)
            nextcoin.targetvalue = tv + r0
            nextcoin.stock = lc.stock
            print(comp)
            print(lc.value)
            print(nextcoin.value)
            nextcoin.save()