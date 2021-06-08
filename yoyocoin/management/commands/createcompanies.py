from django.core.management.base import BaseCommand, CommandError
import random
import decimal
import datetime
from yoyocoin.models import Company, Value, Tweet

comp = [
    ["Big Miss Steak: Pixel-Team","STEAK"],
    ["I Will Win The GMC Jam 41. The Winner For The Worst Game. Mark My Words!!!!: Cantavanda","CANTA"],
    ["Robozoiz Park: GameDevDan","ROBO"],
    ["Fjootjah Sk8: Bart","FJOOT"],
    ["Van Helsing's Big Missed Stake: Mr Magnus","HELS"],
    ["Evanski's Raccoon Adventure: EvanSki","EVAN"],
    ["The Secret and the Bread: Josh Chen","BREAD"],
    ["A Small Mistake: Ericbomb","SMALL"],
    ["Pursuit: BluishGreenPro","PURS"],
    ["E.T 2021: kburkhart84","ET21"],
    ["Game COLD: Toque","COLD"],
    ["Fish Food: SoapSud39","FISH"],
    ["A Tentacle With A Knife: BreakfastBoy","KNIFE"],
    ["Magic's Final Stand: The M","MAGIC"],
    ["Super Ordinary Borthers: Yal","SUPER"],
    ["Catch The Damn Clown: Nocturne","CLOWN"],
    ["Shadow Bouncer: Jordan Ottesen","BOUNCE"],
    ["Shroom Boy: Poizen","SHROOM"],
    ["Lens Of The Last Surviving Human: Mercerenies","LENS"],
    ["Wheel Chair Joyride: Terminator_Pony","WHEEL"],
    ["There Is Going To Be A Bomb: Bearman_18","BOMB"],
    ["I, T'Kemsa: Siolfor The Jackal","TKEMSA"],
    ["YoYoCoin Market: Mr MAgnus","MARKET"],
    ["Mosquitattoos: Yozoraki","TATTOO"],
    ["BOOM!: Alice","BOOM"],
]

class Command(BaseCommand):
    help = 'Updates the YoYocoin base value'

    def handle(self, *args, **options):
        global comp 
        for corp in comp:
            c = Company()
            c.name = corp[0]
            c.code = corp[1]
            c.shares = 5000
            c.baseshares = 5000
            c.mediaDrive = 0.1
            c.save()

            v = Value()
            v.time = datetime.datetime.now()
            v.value = 100
            v.stock = c
            v.basevalue = 100
            v.targetvalue = 100
            v.save()
