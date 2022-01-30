from django.db import models
from django.db.models import F
from django.db.models.expressions import OuterRef, Subquery
from django.utils import timezone
from datetime import datetime, timedelta

from django.db.models import Avg
from django.db.models.aggregates import Max 

class highScore(models.Model):
    userCode = models.CharField(max_length=99)
    platform = models.CharField(max_length = 10, default="WINDOWS")
    user = models.CharField(max_length=99)
    mode = models.CharField(max_length=7)
    height = models.IntegerField()
    rooms = models.IntegerField(default = 0)
    date = models.DateTimeField(auto_now = True)
    class Meta:
       indexes = [
           models.Index(fields=['date']),
           models.Index(fields=['height']),
           models.Index(fields=['rooms']),
    ]

    @staticmethod
    def Serialize(set):
        return [x.serialize() for x in set]

    @staticmethod
    def getBestResults(mode, date = None):
        set = highScore.objects.filter(mode = mode)
        if(date):
            set = set.filter(date__gt = date)
        return set
        
    @staticmethod
    def bestUniqueResults(set, field, p, n):
        tall_sq = set.filter(
            userCode=OuterRef("userCode")
        ).order_by("-"+field)

        return set.annotate(
            best=Subquery(
                tall_sq.values(field)[:1]
            ),
            recent = Subquery(
                tall_sq.values("date")[:1]
            )
        ).filter(best = F(field), recent = F("date")).order_by("-"+field).distinct()[:n]

    @staticmethod
    def getHighscoreLists(mode, page, n):

        allTime = highScore.getBestResults(mode)
        thisMonth = highScore.getBestResults(mode, timezone.make_aware(datetime.now() - timedelta(days = 30)))
        thisWeek = highScore.getBestResults(mode,timezone.make_aware(datetime.now() - timedelta(days = 7)))
        today = highScore.getBestResults(mode,timezone.make_aware(datetime.now() - timedelta(hours = 24)))

        res_allTime =  highScore.bestUniqueResults(allTime,'height',page,n) |  highScore.bestUniqueResults(allTime,'rooms',page,n)
        res_month =  highScore.bestUniqueResults(thisMonth,'height',page,n) | highScore.bestUniqueResults(thisMonth,'rooms',page,n)
        res_week =  highScore.bestUniqueResults(thisWeek,'height',page, n) | highScore.bestUniqueResults(thisWeek,'rooms',page, n)
        res_day =  highScore.bestUniqueResults(today,'height',page,n) | highScore.bestUniqueResults(today,'rooms',page, n)
        r = (res_allTime| res_month | res_week | res_day ).distinct()
        r = r.order_by("-height")
        results = highScore.Serialize(r)
        
        return results

    @staticmethod
    def getAverages(mode):        
        allTime = highScore.getBestResults(mode)
        thisMonth = highScore.getBestResults(mode, timezone.make_aware(datetime.now() - timedelta(days = 30)))
        thisWeek = highScore.getBestResults(mode,timezone.make_aware(datetime.now() - timedelta(days = 7)))
        today = highScore.getBestResults(mode,timezone.make_aware(datetime.now() - timedelta(hours = 24)))

        aAll = allTime.aggregate(Avg('height'))
        aMonth = thisMonth.aggregate(Avg('height'))
        aWeek = thisWeek.aggregate(Avg('height'))
        aToday = today.aggregate(Avg('height'))

        mAll = allTime.aggregate(Max('height'))
        mMonth = thisMonth.aggregate(Max('height'))
        mWeek = thisWeek.aggregate(Max('height'))
        mToday = today.aggregate(Max('height'))

        return [
            highScore.formatAverage(aAll, "All Time Average"),
            highScore.formatAverage(aMonth, "Monthly Average"),
            highScore.formatAverage(aWeek, "Weekly Average"),
            highScore.formatAverage(aToday, "Daily Average"),
            highScore.formatAverage(mAll, "All Time Best","max"),
            highScore.formatAverage(mMonth, "Monthly Best", "max"),
            highScore.formatAverage(mWeek, "Weekly Best", "max"),
            highScore.formatAverage(mToday, "Daily Best", "max")
        ]

    @staticmethod 
    def getUserData(mode, user):                
        r = {
            "results":[]
        }
        allTime = highScore.getBestResults(mode)     
        thisMonth = highScore.getBestResults(mode, timezone.make_aware(datetime.now() - timedelta(days = 30)))
        thisWeek = highScore.getBestResults(mode,timezone.make_aware(datetime.now() - timedelta(days = 7)))
        today = highScore.getBestResults(mode,timezone.make_aware(datetime.now() - timedelta(hours = 24)))

        myRecords = allTime.filter(userCode = user)  

        avg = {}
        tall = {}
        wide = {}
        avg['all'] = allTime.filter(userCode = user).aggregate(Avg('height'))
        tall['all'] = allTime.filter(userCode = user).aggregate(Max('height'))
        wide['all'] = allTime.filter(userCode = user).aggregate(Max('rooms'))

        tall['month'] = thisMonth.filter(userCode = user).aggregate(Max('height'))
        tall['week'] = thisWeek.filter(userCode = user).aggregate(Max('height'))
        tall['day'] = today.filter(userCode = user).aggregate(Max('height'))
        
        wide['month'] = thisMonth.filter(userCode = user).aggregate(Max('rooms'))
        wide['week'] = thisWeek.filter(userCode = user).aggregate(Max('rooms'))
        wide['day'] = today.filter(userCode = user).aggregate(Max('rooms'))

        r['results'].append(highScore.formatAverage(avg['all'],"Your Average"))
        r['results'].append(highScore.formatAverage(tall['all'],"Your Best", "max"))
        u = {
            'ta' : [tall['all']['height__max'] or 0, allTime.filter(height__gt = tall['all']['height__max'] or 0).count()+1],
            'tm' : [tall['month']['height__max'] or 0, thisMonth.filter(height__gt = tall['month']['height__max'] or 0).count()+1],
            'tw' : [tall['week']['height__max'] or 0, thisWeek.filter(height__gt = tall['week']['height__max'] or 0).count()+1],
            'td' : [tall['day']['height__max'] or 0, today.filter(height__gt = tall['day']['height__max'] or 0).count()+1],
            'wa' : [wide['all']['rooms__max'] or 0, allTime.filter(rooms__gt = wide['all']['rooms__max'] or 0).count()+1],
            'wm' : [wide['month']['rooms__max'] or 0, thisMonth.filter(rooms__gt = wide['month']['rooms__max'] or 0).count()+1],
            'ww' : [wide['week']['rooms__max'] or 0, thisWeek.filter(rooms__gt = wide['week']['rooms__max'] or 0).count()+1],
            'wd' : [wide['day']['rooms__max'] or 0, today.filter(rooms__gt = wide['day']['rooms__max'] or 0).count()+1]
        }

        r['u'] = u

        return r
        
    @staticmethod
    def formatAverage(average, label, field = 'avg'):    
        return {"uid":"X","u":label,"h":average['height__'+field] or 0,"r":None, "d":None}
    def serialize(self):
        return {"uid":self.userCode, "u": self.user.strip(), "h":self.height, "r":self.rooms, "d":self.date}

