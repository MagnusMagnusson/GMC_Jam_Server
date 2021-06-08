"""gmc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from jam_40 import views as jam40
from yoyocoin import views as yoyocoin

def ping(request):
    return JsonResponse({"result":True})

urlpatterns = [
    path('ping', ping),
    path('jam40/player', jam40.player ),
    path('jam40/player/rename', jam40.player_rename ),
    path('jam40/attempt/stats', jam40.attemptStat ),
    path('jam40/attempt', jam40.attempt ),

    
    path('yoyocoin/market', yoyocoin.getMarket ),
    path('yoyocoin/news', yoyocoin.getNews ),
    path('yoyocoin/auth/register', yoyocoin.register ),
    path('yoyocoin/auth/login', yoyocoin.login ),
    path('yoyocoin/user/<slug:user>/shares', yoyocoin.userShares ),
    path('yoyocoin/order/buy', yoyocoin.buy),
    path('yoyocoin/order/sell', yoyocoin.sell),
    path('yoyocoin/companies', yoyocoin.companies),
    path('yoyocoin', yoyocoin.template),
]
