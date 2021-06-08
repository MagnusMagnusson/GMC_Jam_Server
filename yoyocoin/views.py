from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

from django.template import loader
from yoyocoin.models import Company, Value, Tweet, Investor, Transaction
from yoyocoin.secrets import APIKEY
import decimal
import hashlib
from datetime import datetime, tzinfo
from datetime import timedelta, timezone
import json
import random

# Create your views here.

def getMarket(request):
    companies = Company.objects.all()
    data = [
        {
            "name": c.name,
            "shares": c.code,
            "history":[
                {
                    "value" : v.value
                }
                for v in c.value_set.filter(time__gte =  (datetime.now() - timedelta(days = 1)))
            ][::3]
        }
            for c in companies
    ]
    return JsonResponse({"data":data})

def getNews(request):
    tweets = Tweet.objects.all().filter(time__lte = datetime.now())
    blurp = {"tweets":[{"time":x.time, "title":x.title,"clip":x.clip} for x in tweets][-6:]}
    return JsonResponse({"data":blurp})

def buy(request):
    body = request.body.decode('utf-8')
    post = json.loads(body)
    print(body)
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
    t.stock = code
    t.amount = shareAmount
    t.price = val
    t.save()

    investor.money -= decimal.Decimal(amount)
    investor.save()

    company.shares += shareAmount
    company.save()

    return JsonResponse({"success":True, "data":{
        "share": code,
        "price" : val,
        "bought" : shareAmount, 
        "paid" : amount
    }})

def sell(request):
    body = request.body.decode('utf-8')
    post = json.loads(body)
    print(body)
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


    owned = investor.getShare(code)
    print("owned")
    print(owned[0]["amount__sum"])
    print(amount)
    if len(owned) == 0 or owned[0]["amount__sum"] < amount:
        return JsonResponse({"success":False})

    val = share.value
    amount = decimal.Decimal(amount)
    moneyAmount = amount * val
    t = Transaction()
    t.time = datetime.now()
    t.investor = investor 
    t.stock = code
    t.amount = -amount
    t.price = val
    t.save()

    investor.money += decimal.Decimal(moneyAmount) 
    investor.save()

    company.shares -= amount
    company.save()

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
        print(h)
        print(investor.password)
        if(str(h) == investor.password):
            print("yes")
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
            "money":round(x.money,2),
            "portfolio": round(x.getWorth(),2),
            "total": round(x.money + x.getWorth(),2)
        } for x in all
    ]
    l.sort(key = s)
    d = {"investors": l}
    return d

def valueChart():
    companies = Company.objects.all()
    yesterday = (datetime.utcnow() - timedelta(days = 1))
    data = [
        {
            "label": c.code,
            "data":[ v.value for v in c.value_set.filter(time__gte = yesterday)][::5],
            "fill":False,
            "tension":0.1,
            "borderColor": 'rgb('+str(random.random() * 255)+","+str(random.random() * 255)+","+str(random.random() * 255)+")"
        }
        for c in companies
    ]
    return data


def template(request):

    template = loader.get_template('test.html')
    context = get_leaderboard()
    context["history"] = valueChart() 

    tweets = Tweet.objects.all().filter(time__lte = datetime.utcnow())
    blurp = [{"time":x.time, "title":x.title,"clip":x.clip} for x in tweets][-6:]
    
    context["tweets"] = blurp
    return HttpResponse(template.render(context, request))
