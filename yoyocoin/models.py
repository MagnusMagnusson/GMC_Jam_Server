from django.db import models
from django.db.models import  Sum, base, F
import decimal
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.db import transaction

# Create your models here.

class Investor(models.Model):
    name = models.CharField(max_length = 64)
    username = models.CharField(max_length = 64, primary_key = True)
    password = models.CharField(max_length = 256)
    salt = models.CharField(max_length=256)
    token = models.CharField(max_length=256)
    money = models.DecimalField(default = 10000, decimal_places=2, max_digits=65)

    def getShares(self):
        transactions = self.transaction_set.all().values("stock__code").annotate(Sum("amount")).values("amount__sum", stock = F("stock__code"))
        return [x for x in transactions]
    def getShare(self, company):
        transactions = self.transaction_set.filter(stock = company).values("stock__code").annotate(Sum("amount")).values("amount__sum", stock = F("stock__code"))
        return [x for x in transactions]
    def getWorth(self):
        shares = self.getShares()
        t = 0
        for s in shares:
            code = s["stock"]
            value = Value.objects.filter(stock__code = code).latest('id')
            t += decimal.Decimal(s["amount__sum"]) * value.value
        return t

class Company(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length = 5)
    shares = models.DecimalField(max_digits=65, decimal_places=2)
    baseshares = models.DecimalField(max_digits=65, decimal_places=2, default = 10000)
    mediaDrive = models.FloatField()

    def updatePrice(self):
        aff = self.transaction_set.values("investor").annotate(amount = Sum("amount")).filter(amount__gte = 0.01)
        s = 0
        for inv in aff:
            s += min(decimal.Decimal(0.05) * self.baseshares, inv["amount"]) #Each investor can add at most 5% to the demand of any stock

        latest = self.value_set.all().latest("time")
        prevTime = latest.time
        now = timezone.now()
        aMinute = timedelta(minutes = 1)
        i = 0
        while(prevTime < now):
            if i % (60*24) == 0:
                print(prevTime)
            i += 1
            r0 = decimal.Decimal(random.random()*random.random() * 1 - random.random()*random.random()*0.95)
            r1 = decimal.Decimal(random.randint(30,90))
            #tweets = Tweet.objects.all().filter(time__lte = now).filter(time__gte = latest.time)
            vc = 0
            #for tweet in tweets:
            #    vc += tweet.valueChange
            tv = latest.targetvalue + vc * decimal.Decimal(self.mediaDrive)

            nextcoin = Value()
            basevalue = latest.basevalue + ((tv * decimal.Decimal((self.shares + s)/self.baseshares) - latest.basevalue)/r1)
            if basevalue < 0:
                basevalue /= 2
            nextcoin.basevalue = basevalue
            nextcoin.value = max(1, basevalue)
            nextcoin.targetvalue = tv + r0
            nextcoin.stock = latest.stock
            nextcoin.time = prevTime + aMinute
            nextcoin.save()

            latest = nextcoin
            prevTime += aMinute

    @staticmethod 
    def updateAllPrices():
        now = datetime(2021, 6, 21, 12, 0, 0)
        if not settings.DEBUG and (datetime(2021, 6, 21, 12, 0, 0) < datetime.now() or now < datetime(2021, 6, 14, 12, 0, 0)):
            return False
        latest = Value.objects.all().latest("time").time
        now = timezone.now()
        latest = latest.replace(second = 0, microsecond = 0)
        now = now.replace(second = 0, microsecond = 0)
        if latest < now:
            with transaction.atomic():
                for comp in Company.objects.all():
                    comp.updatePrice()
            print("committed")

class Value(models.Model):
    time = models.DateTimeField(default=timezone.now)
    value = models.DecimalField(decimal_places=2, max_digits=65)
    stock = models.ForeignKey(Company, on_delete=models.CASCADE)
    basevalue = models.DecimalField(decimal_places=2, max_digits=65)
    targetvalue = models.DecimalField(decimal_places=2, max_digits=65)
    class Meta:
       indexes = [
           models.Index(fields=['time']),
    ]
    

class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    stock = models.CharField(max_length=10)
    amount = models.DecimalField(decimal_places=2, max_digits=65)
    price = models.DecimalField(decimal_places=2, max_digits=65)

class Tweet(models.Model):
    id = models.AutoField(primary_key = True)
    time = models.DateTimeField()
    title = models.CharField(max_length=64)
    clip = models.CharField(max_length=256)
    valueChange = models.DecimalField(decimal_places=2, max_digits=65)