from django.core.management.base import BaseCommand, CommandError
import random
import decimal
import datetime
from yoyocoin.models import Company, Value, Tweet

class Command(BaseCommand):
    help = 'Updates the YoYocoin base value'


    def handle(self, *args, **options):
        codes = [
            "BOMB",
            "ROBO",
            "BOOM",
            "STEA",
            "PURS",
            "FISH",
            "MAGI",
            "HELS",
            "TKEM",
            "BOUN",
            "KNIF",
            "FJOO",
            "COLD",
            "LENS",
            "MARK",
            "BREA",
            "EVAN",
            "TATT",
            "WHEE",
            "SMAL",
            "ET21",
            "SHRO",
            "SUPE",
            "CANT",
        ]
        pos = 0
        for code in codes:
            corp = Company.objects.get(code = code)
            print(corp.name, pos)
            corp.baseshares += 2 * (pos - 1)
            corp.shares += 23
            corp.save()
            pos += 1
