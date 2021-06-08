from django.core.management.base import BaseCommand, CommandError
import random
import decimal
import datetime
from yoyocoin.models import Company, Value, Tweet

class Command(BaseCommand):
    help = 'Updates the YoYocoin base value'

    def handle(self, *args, **options):
        comp = Company.objects.all()
        for corp in comp:
            if(corp.baseshares == 5000):
                corp.shares -= 4000
                corp.baseshares -= 4000
                corp.save()
