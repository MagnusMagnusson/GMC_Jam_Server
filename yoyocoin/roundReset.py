from .models import *
from .tweets import firstTweet, lastTweet, getTweets
from django.utils import timezone
from datetime import datetime, timedelta

def burnDatabase():
    Value.objects.all().delete()
    Transaction.objects.all().delete()
    Tweet.objects.all().delete()

def resetMoney():
    investors = Investor.objects.all()
    for i in investors:
        i.money = 10000
        i.save()

def resetCompanyShares():
    companies = Company.objects.all()
    for c in companies:
        if c.code == "yoyo":
            c.baseshares = 5000
            c.shares = 5000
            c.mediaDrive = 1
        else:
            c.baseshares = 2000
            c.shares = 2000
            c.mediaDrive = 0.4
        c.save()

def initSharePrice():
    companies = Company.objects.all()
    for c in companies:
        v = Value()
        v.stock = c
        if c.code == "yoyo":
            v.value = 500
            v.basevalue = 500
            v.targetvalue = 500
        else:
            v.value = 100
            v.basevalue = 100
            v.targetvalue = 100
        v.time = timezone.make_aware(datetime.now() - timedelta(days = 7))
        print(v.time)
        v.save()

def populateNews():
        now = timezone.make_aware(datetime(2021, 6, 14, 12, 00, 00))
        stop = timezone.make_aware(datetime(2021, 6, 21, 11, 30, 00))
        
        t0 = Tweet()
        t0.time = now
        t0.title = firstTweet["title"]
        t0.clip = firstTweet["clip"]
        t0.valueChange = firstTweet["valueChange"]
        t0.save()


        tweets = getTweets()
        random.shuffle(tweets)
        i = 0
        while now < stop:
            delta = timedelta(minutes=random.randrange(5, 65))
            now = now + delta 
            chirp = tweets[i]
            t = Tweet()
            t.time = now
            t.title = chirp["title"]
            t.clip = chirp["clip"]
            t.valueChange = chirp["valueChange"]
            t.save()
            i = i + 1
            if(len(tweets) <= i):
                random.shuffle(tweets)
                i = 0
        
        t1 = Tweet()
        t1.time = timezone.make_aware(datetime(2021, 6, 21, 12, 00, 00))
        t1.title = lastTweet["title"]
        t1.clip = lastTweet["clip"]
        t1.valueChange = lastTweet["valueChange"]
        t1.save()  

def open():
    # this function doesn't do anything, it's just for the screenshot
    print("The market is open!")