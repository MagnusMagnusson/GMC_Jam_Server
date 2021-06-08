from django.http import JsonResponse
from jam_40.models import Person, Attempt
import random
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def player(request):
    p = Person.objects.all().filter(key = request.GET['userKey'])
    if(len(p) == 1):
        return JsonResponse({'name': p[0].name,'salt': p[0].salt, 'key': p[0].key})
    else:
        p = Person()
        p.key = request.GET['userKey']
        p.name = "Unknown Guest"
        p.salt = str(random.randint(10000, 100000))
        p.save()
        return JsonResponse({'name': p.name, 'salt' : p.salt, 'key': p.key})
        
@csrf_exempt
def attempt(request):
    if(request.method == "POST"):
        body = request.body.decode('utf-8')
        post = json.loads(body)
        if(post['api_key'] != settings.API_KEY):
            return JsonResponse({"success":False, "reason":"INVALID API KEY"}, 401)
        if("gamemode" in post and "userKey" in post and "_score" in post and "attemptNr" in post):
            p = Person.objects.all().filter(key = post['userKey'])
            if(len(p) == 1):
                print(30)
                p = p[0]
                a = Attempt()
                a.player = p
                a.gamemode = post['gamemode']
                a.score = post['_score']
                if(post['subscore']):
                    a.subscore = post['subscore']
                a.attemptNr = post['attemptNr']
                now = datetime.now()
                a.date = now
                a.save()
    else:
        gamemode = request.GET['gamemode']
        sortFunction = None
        if gamemode == 'marathon':
            sortFunction = lambda a : (10000  * a.score) + (a.subscore if a.subscore else 0)
        else:
            sortFunction = lambda a : -a.score
        return JsonResponse({"recent":Attempt.recent(gamemode), "top":Attempt.top(gamemode, sortFunction)})
    return JsonResponse({})

@csrf_exempt
def player_rename(request):
    if(request.method == "POST"):
        body = request.body.decode('utf-8')
        post = json.loads(body)
        if(post['api_key'] != settings.API_KEY):
            return JsonResponse({"success":False, "reason":"INVALID API KEY"}, 401)
        userKey = post['userKey']
        p = Person.objects.all().filter(key = userKey)
        if(len(p) == 1):
            p[0].name = post['name']
            p[0].save()

def attemptStat(request):
    return JsonResponse(Attempt.statistics(request.GET['gamemode']))
