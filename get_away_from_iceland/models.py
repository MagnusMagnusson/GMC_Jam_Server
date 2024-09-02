from django.db import models


class highScore(models.Model):
    name = models.CharField(max_length=99)
    score = models.IntegerField()
    uid = models.CharField(max_length=99)
    date = models.DateTimeField(auto_now = True)
    run = models.TextField(max_length=4000)
    hash = models.CharField(max_length=128)
    class Meta:
       indexes = [
           models.Index(fields=['date']),
           models.Index(fields=['score']),
    ]