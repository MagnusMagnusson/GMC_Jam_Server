from django.db import models
from django.db.models import  Sum
import decimal

# Create your models here.

class Investor(models.Model):
    name = models.CharField(max_length = 64)
    username = models.CharField(max_length = 64, primary_key = True)
    password = models.CharField(max_length = 256)
    salt = models.CharField(max_length=256)
    token = models.CharField(max_length=256)
    money = models.DecimalField(default = 10000, decimal_places=2, max_digits=65)

    def getShares(self):
        transactions = self.transaction_set.all().values("stock").annotate(Sum("amount")).order_by()
        return [x for x in transactions]
    def getShare(self, code):
        transactions = self.transaction_set.filter(stock = code).values("stock").annotate(Sum("amount"))
        print(transactions)
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

class Value(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(decimal_places=2, max_digits=65)
    stock = models.ForeignKey(Company, on_delete=models.CASCADE)
    basevalue = models.DecimalField(decimal_places=2, max_digits=65)
    targetvalue = models.DecimalField(decimal_places=2, max_digits=65)
    

class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    stock = models.CharField(default="yoyo", max_length=64)
    amount = models.DecimalField(decimal_places=2, max_digits=65)
    price = models.DecimalField(decimal_places=2, max_digits=65)

class Tweet(models.Model):
    id = models.AutoField(primary_key = True)
    time = models.DateTimeField()
    title = models.CharField(max_length=64)
    clip = models.CharField(max_length=256)
    valueChange = models.DecimalField(decimal_places=2, max_digits=65)