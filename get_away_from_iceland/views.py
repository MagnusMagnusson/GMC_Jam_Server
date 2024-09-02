from datetime import datetime
from django.shortcuts import render
from django.views import View
from get_away_from_iceland.models import highScore
from django.http import JsonResponse
import json
import re
import random

profanities = [
    "tit",
    "dick",
    "cunt",
    "pussy",
    "fuck",
    "boob",
    "crap",
    "shit",
    "nigger",
    "slut",
    "faggot",
    "fag",
    "sex",
    "bitch",
    "boob",
    "vagina",
    "penis"
]

birds = [
    "duck",
    "swan",
    "loom",
    "goose",
    "robin",
    "pidgeon",
    "ptarmigan",
    "ptarmigan",
    "parrot",
    "puffin",
    "owl",
    "warbler",
    "hummingbird",
    "redwing",
    "starling",
    "swift",
    "osprey"
]

class Highscores(View):
    def get(self, request, mode):
        h = highScore.objects.filter(hash = mode)
        d = {
            "results" : [
                {
                    "name" : p.name,
                    "score" : p.score,
                    "run" : p.run,
                    "uid" : p.uid,
                }
                for p in h
            ]
        }
        return JsonResponse(d)

    def post(self, request, mode):
        p = json.loads(request.body) 

        test = highScore.objects.filter(uid = p["uid"], hash = mode)
        if(test.exists()):
            h = highScore.objects.get(uid = p["uid"], hash = mode)
            s = p["score"]
            if s > h.score:
                h.score = s
                h.run = p["run"]
                h.date = datetime.now()
                name = p["name"]
                for prof in profanities:
                    pattern = re.compile(prof, re.IGNORECASE)
                    name = pattern.sub(random.choice(birds), name)
                h.name = name
                h.save()
                return JsonResponse({
                    "improvement": True
                })
            else:
                return JsonResponse({
                    "improvement": False
                })
        else: 
            h = highScore()
            h.uid = p["uid"]
            h.name = p["name"]
            h.run = p["run"]
            h.hash = mode
            h.score = p["score"] 
            h.save()
        return JsonResponse({
            "improvement": True
        })
