from django.shortcuts import render
from django.views import View
from jam42_babel.models import highScore
from django.http import JsonResponse
import json
import re

def formatAverage(average, label, field = 'avg'):
    return {"uid":"X","u":label,"h":average['height__'+field],"r":None, "d":None}

legalModes = [
    "classic","modern","acrobat","standar"
]

class Highscores(View):
    def get(self, request, mode):
        if(not mode in legalModes):
            return JsonResponse({"error":"Not a valid mode"}, status = 404)
        try:
            page = int(request.GET['page']) if 'page' in request.GET else 0
        except Exception:
            page = 0
        n = 15
        results = highScore.getHighscoreLists(mode, page, n)
        results += highScore.getAverages(mode)

        d = {
            "r":results,
            "m":mode
        }

        return JsonResponse(d)

    def post(self, request, mode ):
        if(not mode in legalModes):
            return JsonResponse({"error":"Not a valid mode"}, status = 404)
        profanities = [
            "tit",
            "dick",
            "cunt",
            "pussy",
            "ass",
            "fuck",
            "boob",
            "crap",
            "shit",
            "nigger",
            "slut",
            "faggot",
            "fag"
        ]
        p = json.loads(request.body) 
        h = highScore()
        h.userCode = p["uid"]
        h.user = p["user"]
        for prof in profanities:
            pattern = re.compile(prof, re.IGNORECASE)
            h.user = pattern.sub("duck", h.user)
        h.height = p["height"]
        h.rooms = p["rooms"]
        h.mode = p["mode"] 
        h.platform = p["platform"] 
        h.save()
        return JsonResponse({
            "r":h.serialize(),
            "m":mode
        })

class Users(View):
    def get(self, request, mode, uid):
        if(not mode in legalModes):
            return JsonResponse({"error":"Not a valid mode"}, status = 404)
        res = {
            "u":highScore.getUserData(mode, uid),
            "m":mode
        }
        return JsonResponse(res)
