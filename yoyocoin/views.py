from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings

from django.template import loader
from yoyocoin.models import Company, Value, Tweet, Investor, Transaction
from yoyocoin.secrets import APIKEY
import decimal
import hashlib
from datetime import datetime, tzinfo
from datetime import timedelta
from django.utils import timezone 
import json
import random

# Create your views here.

def getMarket(request):
    Company.updateAllPrices() # Lazy Price Updating
    companies = Company.objects.all()
    values = Value.objects.filter(time__gte = timezone.make_aware(datetime.now() - timedelta(days = 1)))
    print(len(values))
    cl = {}
    for c in companies:
        cl[c.id] = []
    for v in values:
        cl[v.stock_id].append({"value":v.value})
    data = [
        {
            "name": c.name,
            "shares": c.code,
            "history":cl[c.id]
        }
            for c in companies
    ]
    return JsonResponse({"data":data})

def getNews(request):
    tweets = Tweet.objects.all().filter(time__lte = datetime.now())
    blurp = {"tweets":[{"time":x.time, "title":x.title,"clip":x.clip} for x in tweets][-6:]}
    return JsonResponse({"data":blurp})

def buy(request):
    Company.updateAllPrices() # Lazy Price Updating
    now = datetime(2021, 6, 21, 12, 0, 0)
    if not settings.DEBUG and (datetime(2021, 6, 21, 12, 0, 0) < datetime.now() or now < datetime(2021, 6, 14, 12, 0, 0)):
        return JsonResponse({"success":False})

    body = request.body.decode('utf-8')
    post = json.loads(body)
    if(post["apikey"] != APIKEY):
        return JsonResponse({"success":False})
    token = post['token']
    username = post['username']
    code = post['share']
    amount = post['amount']
    investor = Investor.objects.all().filter(token = token, username = username)
    if(len(investor) != 1):
        return JsonResponse({"success":False})
    investor = investor[0]

    if amount > investor.money:
        return JsonResponse({"success":False})


    company = Company.objects.get(code = code)
    share = company.value_set.order_by("-time")[0]

    val = share.value
    amount = decimal.Decimal(amount)
    shareAmount = amount / val
    t = Transaction()
    t.time = datetime.now()
    t.investor = investor
    t.stock = company
    t.amount = shareAmount
    t.price = val
    t.save()

    investor.money -= decimal.Decimal(amount)
    investor.save()

    return JsonResponse({"success":True, "data":{
        "share": code,
        "price" : val,
        "bought" : shareAmount, 
        "paid" : amount
    }})

def sell(request):
    Company.updateAllPrices() # Lazy Price Updating
    now = datetime(2021, 6, 21, 12, 0, 0)
    if not settings.DEBUG and (datetime(2021, 6, 21, 12, 0, 0) < datetime.now() or now < datetime(2021, 6, 14, 12, 0, 0)):
        return JsonResponse({"success":False})

    body = request.body.decode('utf-8')
    post = json.loads(body)
    if(post["apikey"] != APIKEY):
        return JsonResponse({"success":False})
    token = post['token']
    username = post['username']
    code = post['share']
    amount = post['amount']
    investor = Investor.objects.all().filter(token = token, username__iexact = username)
    if(len(investor) != 1):
        return JsonResponse({"success":False})
    
    investor = investor[0]


    company = Company.objects.get(code = code)
    share = company.value_set.order_by("-time")[0]


    owned = investor.getShare(company)
    if len(owned) == 0 or owned[0]["amount__sum"] < amount:
        return JsonResponse({"success":False})

    val = share.value
    amount = decimal.Decimal(amount)
    moneyAmount = amount * val
    t = Transaction()
    t.time = datetime.now()
    t.investor = investor 
    t.stock = company
    t.amount = -amount
    t.price = val
    t.save()

    investor.money += decimal.Decimal(moneyAmount) 
    investor.save()

    return JsonResponse({"success":True, "data":{
        "share": code,
        "price" : val,
        "sold" : amount, 
        "earned" : moneyAmount
    }})

def companies(request):
    c = Company.objects.all()
    
    return JsonResponse({"data":[{
        "name":x.name,
        "code":x.code
    }
    for x in c]})


def userShares(request, user):
    investor = Investor.objects.all().filter(username__iexact = user)
    if(len(investor) == 1):
        transactions = investor[0].getShares()
        print(transactions)
        return JsonResponse({"money":investor[0].money,"shares":transactions})
    return JsonResponse({"data":len(investor)})

def login(request):
    body = request.body.decode('utf-8')
    post = json.loads(body)
    if(post['apikey'] != APIKEY):
        return JsonResponse({"success":False})
    user = post['username']
    password = post['password']
    investor = Investor.objects.all().filter(username__iexact = user)
    if user == "":
        return JsonResponse({"success":False})
    if(len(investor) == 1):
        investor = investor[0]
        m = hashlib.sha256()
        m.update(bytes(password,"utf-8"))
        m.update(bytes(investor.salt,"utf-8"))
        h = m.digest()
        if(str(h) == investor.password):
            return JsonResponse({"success":True, "user": {
                "name": investor.name,
                "user": investor.username,
                "token": investor.token,
                "money": investor.money,
                "shares": []
            }})
    return JsonResponse({"success":False})

def register(request):
    body = request.body.decode('utf-8')
    post = json.loads(body)
    print(body)
    if(post["apikey"] != APIKEY):
        return JsonResponse({"success":False})
    investor = Investor()
    
    user = post["username"]
    password = post["password"]
    if user == "" or password == "":
        return JsonResponse({"success":False})
    
    _i = Investor.objects.all().filter(username__iexact = user)
    if(len(_i) > 0):
        return JsonResponse({"success":False})


    investor.name = user
    investor.username = user
    investor.salt = ''.join(random.choice("qwertyuiopasdfghjklzxcvnmbQWERTYUIOPASDFGHJKLZXCVBNM123456789-_") for i in range(64))
    investor.token = ''.join(random.choice("qwertyuiopasdfghjklzxcvnmbQWERTYUIOPASDFGHJKLZXCVBNM123456789-_") for i in range(64))
    investor.save()

    investor = Investor.objects.all().get(username__iexact = user)
    m = hashlib.sha256()
    m.update(bytes(password,"utf-8"))
    m.update(bytes(investor.salt, "utf-8"))
    h = m.digest()
    investor.password = h
    investor.save()
    
    return JsonResponse({"success":True, "user": {
        "name": investor.name,
        "user": investor.username,
        "token": investor.token,
        "money": investor.money,
        "shares":[]
    }})


def getInvestors(request):
    all = Investor.objects.all()
    d = {"investors": [
        {"name":x.name,
            "money":x.money
        } for x in all
    ]}
    return JsonResponse(d)

def get_leaderboard():
    def s(e):
        return -(e["money"] + e["portfolio"])
    all = Investor.objects.all()
    l = [
        {"name":x.name,
            "money":x.money,
            "portfolio": x.getWorth(),
            "total": x.money + x.getWorth()
        } for x in all
    ]
    l.sort(key = s)
    d = {"investors": l}
    return d

def valueChart():
    companies = Company.objects.all()
    values = Value.objects.filter(time__gte = timezone.make_aware(datetime.now() - timedelta(days = 1)))[::12]
    cl = {}
    for c in companies:
        cl[c.id] = []
    for v in values:
        cl[v.stock__id].append(v.value)

    data = [
        {
            "label": c.code,
            "data":cl[c.id],
            "fill":False,
            "tension":0.1,
            "borderColor": 'rgb('+str(random.random() * 255)+","+str(random.random() * 255)+","+str(random.random() * 255)+")"
        }
        for c in companies
    ]
    return data


def template(request):
    Company.updateAllPrices() # Lazy Price Updating
    template = loader.get_template('test.html')
    context = get_leaderboard()
    context["history"] = valueChart() 

    tweets = Tweet.objects.all().filter(time__lte = datetime.utcnow())
    blurp = [{"time":x.time, "title":x.title,"clip":x.clip} for x in tweets][-6:]
    
    context["tweets"] = blurp
    return HttpResponse(template.render(context, request))
