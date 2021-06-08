from django.core.management.base import BaseCommand, CommandError
import random
import decimal
import datetime
from yoyocoin.models import Company, Value, Tweet

baseShares = 10000
startValue = 100

class Command(BaseCommand):
    help = 'Updates the YoYocoin base value'

    def handle(self, *args, **options):
        yoyo = Company()
        yoyo.name = "YoYoCoin"
        yoyo.code = "yoyo"
        yoyo.shares = 20000
        yoyo.baseshares = 20000
        yoyo.mediaDrive = 1
        yoyo.save()

        v = Value()
        v.time = datetime.datetime.now()
        v.value = 100
        v.stock = yoyo
        v.basevalue = 100
        v.targetvalue = 100
        v.save()
