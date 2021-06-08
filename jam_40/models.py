from django.db import models
from django.db.models import Avg
from django.db.models import Max, Min
from django.db.models import Count
import math

class Person(models.Model):
    name = models.CharField(max_length = 30)
    key = models.CharField(primary_key = True, max_length = 128)
    salt = models.CharField(null = False, default = "defau", max_length = 6)

class Attempt(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey('Person', null = False, on_delete = models.CASCADE)
    score = models.FloatField(null = False)
    subscore = models.FloatField(null = False, default = 0)
    attemptNr = models.IntegerField(null = False)
    date = models.DateTimeField()
    gamemode = models.CharField(max_length=30)

    @staticmethod
    def top(gamemode, sortfunction):
        a = [x for x in Attempt.objects.all().filter(gamemode = gamemode)]
        a = sorted(a,key = sortfunction, reverse=True)
        a = a[:25]
        return [{
            "player": x.player.name + " ["+x.player.salt+"]",
            "_score" : x.score,
            "subscore" : x.subscore,
            "attemptNr" : x.attemptNr,
            "date": x.date,
            "gamemode": x.gamemode
        } for x in a]

    @staticmethod
    def recent(gamemode):
        a = [x for x in Attempt.objects.all().filter(gamemode = gamemode).order_by("-date")]
        a = a[:25]
        return [{
            "player": x.player.name + " ["+x.player.salt+"]",
            "_score" : x.score,
            "subscore" : x.subscore,
            "attemptNr" : x.attemptNr,
            "date": x.date,
            "gamemode": x.gamemode
        } for x in a]

    @staticmethod
    def statistics(gamemode):
        a = Attempt.objects.all().filter(gamemode = gamemode)

        avg = a.aggregate(Avg('score'))['score__avg']
        max = a.aggregate(Max('score'))['score__max']
        min = a.aggregate(Min('score'))['score__min']
        count = len(a)
        med = a[int(math.floor(count / 2))].score if count > 0 else 0

        return {
            "avg": avg,
            "max": max,
            "min": min,
            "count": count,
            "med": med
        }

