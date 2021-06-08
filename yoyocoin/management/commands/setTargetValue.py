from django.core.management.base import BaseCommand, CommandError
import random
import decimal
from yoyocoin.models import Yoyocoin

tv = -200

class Command(BaseCommand):
    help = 'Updates the YoYocoin base value'

    def handle(self, *args, **options):
        r0 = decimal.Decimal(random.random()*random.random() * 3 - random.random()*random.random()*1.75)
        latest = Yoyocoin.objects.all().order_by("-time")
    
        lc = latest[0]
        lc.targetvalue = lc.targetvalue + tv
        lc.save()