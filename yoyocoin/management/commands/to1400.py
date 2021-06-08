from django.core.management.base import BaseCommand, CommandError
import random
import decimal
import datetime
from yoyocoin.models import Yoyocoin, Tweet

baseShares = 10000
startValue = 100

class Command(BaseCommand):
    help = 'Updates the YoYocoin base value'

    
    def handle(self, *args, **options):
        r0 = decimal.Decimal(random.random()*random.random() * 3 - random.random()*random.random()*1.75)
        r1 = decimal.Decimal(random.randint(40,80))
        latest = Yoyocoin.objects.all().order_by("-time")
        missing = 1400 - len(latest)
        while missing > 0:
            if(missing % 100 == 0):
                print(missing)
            missing-=1
            lc = Yoyocoin.objects.all().order_by("-time")[0]
            now = datetime.datetime.now()
            tweets = Tweet.objects.all().filter(time__lte = now).filter(time__gte = lc.time)
            vc = 0
            for tweet in tweets:
                vc += tweet.valueChange
            tv = lc.targetvalue + vc
            nextcoin = Yoyocoin()
            basevalue = lc.basevalue + ((tv * decimal.Decimal(lc.shares/baseShares) - lc.basevalue)/r1)
            nextcoin.basevalue = basevalue + r0
            nextcoin.value = max(1, basevalue)
            nextcoin.targetvalue = tv + r0
            nextcoin.shares = lc.shares
            nextcoin.save()