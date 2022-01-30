from django.core.management.base import BaseCommand, CommandError
import random
import decimal
import datetime
from yoyocoin.models import Company, Value, Tweet

class Command(BaseCommand):
    help = 'Updates the YoYocoin base value'


    def handle(self, *args, **options):
        codes = [
            ["BOMB",[1,2,4,11,15,6,1,8,15,14,13,14]],
            ["BOOM",[2,4,3,1,1,3,3,2,1,1,2,5]],
            ["BOUN",[3,6,5,7,1,8,10,2,3,8,4,1]],
            ["BREA",[16,10,12,7,20,10,20,16,19,20,10,9,11]],
            ["CLOW",[23,19,6,19,23,18,22,20,22,23,23,17,21]],
            ["COLD",[11,12,13,13,12,8,18,13,9,7,16,8,12]],
            ["CANT",[24,24,22,24,17,9,24,23,25,25]],
            ["ET21",[15,23,21,12,23,21,18,24,21,15]],
            ["EVAN",[13,8,5,10,15,6,7,17,6,11,6,18,17]],
            ["FISH",[9,14,9,15,2,11,4,1,6,5,5,11,6,2]],
            ["FJOO",[14,7,20,12,9,16,2,12,4,9,22,16,9]],
            ["HELS",[4,9,7,3,5,3,13,8,10,7,1,18]],
            ["KNIF",[12,11,14,11,13,7,1,12,11,12,13,17,14,13]],
            ["LENS",[20,17,16,8,14,5,14,15,16,15,3,16]],
            ["MAGI",[6,2,9,6,4,8,9,7,13,8,5,15]],
            ["MARK",[7,22,18,21,22,15,15,4,3,19,22]],
            ["PURS",[8,5,17,17,13,10,5,11,19,13,3]],
            ["ROBO",[19,13,22,16,11,9,7,19,2,10,14,12,10]],
            ["SUPE",[21,20,23,14,16,10,17,23,22,21,20,21,23]],
            ["STEA",[1,1,2,3,2,2,3,4,1,6,4,5,4]],
            ["SHRO",[10,15,21,18,4,5,22,16,25,11,8]],
            ["SMAL",[17,18,10,17,19,14,20,14,12,19,7,6]],
            ["TATT",[22,16,19,22,18,17,18,9,10,12,20]],
            ["TKEM",[5,3,4,6,8,6,5,4,9,7,2,2,7]],
            ["WHEE",[18,21,15,20,18,14,21,19,21,17,18,20,19]],
        ]
        
        for code in codes:
            corp = Company.objects.get(code = code[0])
            s = corp.shares
            b = corp.baseshares
            for pos in code[1]:
                s += decimal.Decimal(12.5)
                b += pos 

            print(corp.code, corp.shares,corp.baseshares, s,b,corp.shares/corp.baseshares,s/b)
