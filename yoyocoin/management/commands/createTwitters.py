from django.core.management.base import BaseCommand, CommandError
import random
import decimal
import datetime
from yoyocoin.models import Tweet

def tweet(title, clip, valueChange):
    return {
        "title":title,
        "clip":clip,
        "valueChange":valueChange
    }

tweets = [
    #1
    tweet("Raccoon to host jam","Memes expected to increase by 400%", 50),
    tweet("New Module announced!","Indies excited to develop for smartfridges", 25),
    #2
    tweet("Web browser to purchase yoyo!","Exciting new prospects on the horizon", 100),
    tweet("Manual draws ire!","Odd performance issues bother developers", -25),
    #3
    tweet("YYG announce new logo","The gigantic smile sure to spark joy in community", -200),
    tweet("Jam preperations in full swing","Absolutely nothing going wrong", 20),
        #4
    tweet("New Module not working as intended","Was 'Gamemaker Studio Smartcar edition' too ambitious", -100),
    tweet("GMS 3 announced","Initial price to be revealed, community concerned", 75),
        #5
    tweet("Ouya fails","lightweight console underperforming, developers backing off", -50),
    tweet("Former GMC staff a cult leader","Harrowing reports of a time-locked party gone wrong", -20),
        #6
    tweet("Record participation in jam","Good games expected to get thirtieth place at best", 30),
    tweet("Voting system discussion in flames","People sharing videos of animals say this 'is a disgrace'", -45),
        #7
    tweet("Billionaire denounces yoyocoin","People panic-selling", -450),
    tweet("Billionaire loves yoyocoin","People jumping to buy", 350),
        #8
    tweet("people love the memes!","Local animal residents thrilled", 75),
    tweet("Ghosts and cats found to be friends","People not sure of financial effects, but agree is 'very cute'", 5),
        #9
    tweet("Rabid Red Raccoon on a rampage!","Green raccoon claims no association", -75),
    tweet("Noticable lack of cheese in forum","Dairy farmers claim sabotage", -66),
        #10
    tweet("Streamer plays bad game","blames engine.", -100),
    tweet("Streamer plays great game","loves choice of engine.", 50),
        #11
    tweet("Small city devastated by a giant lizard","Claims to have just wanted to see the sights", -20),
    tweet("Switch port a huge success","Handheld games easier to make than ever", 125),
    #12
    tweet("Sandbox to shut down", "Thousands of amature games to be deleted", 60),
    tweet("Forum devestated by gang warfare", "'Most fun we have had in years' claims person", 75),
    #13
    tweet("Local man develops game", "only took fourteen years", 5),
    tweet("Local man develops game", "'dreadfully average'", -10),
    #14
    tweet("New film franchise announced", "loosely based on true events", 40),
    tweet("New film franchise announced", "Reeboots beloved series.", -40),
        #15
    tweet("Film Franchise fails dreadfully", "bland directing and lack of direction to blame", -50),
    tweet("Film Franchise does better than expected", "great lead says it a matter of teamwork", 75),
        #16
    tweet("Delfino Plaza experiences a waterfall-like deluge of rain.", "Residents asked to seek shelter on rooftops", -100),
    tweet("Film Franchise does better than expected", "great lead says it a matter of teamwork", 250),
        #17
    tweet("YoYocoin a success!", "Investors rush to buy shares", 100),
    tweet("Markets florish", "stall across the street gets exotic fruit", 10),
        #18
    tweet("I'm eating food", "It's lentil stew, and very yummy", 10),
    tweet("Headline author tires out", "making dozens of headlines 'a lot of work'", -10),
        #19
    tweet("Old forum deleted", "previous jams now only found on archive.org", -25),
    tweet("Investors getting late in game", "Rising prices makes investing difficult", -5),
        #20
    tweet("Nocturne makes 'mistake of a game'", "Utilizes very old engine", 5),
    tweet("Brand new MMORPG released by Cantavanda", "Had to delay release to not miss bedtime", -100),
        #21
    tweet("Jam well attended", "Many fanatstic games compete", 90),
    tweet("Forum Mafia in decline", "Hardly anyone lynched these days", -50),
        #22
    tweet("Vampires on the run", "Local vampire hunter staking success on eradication", 66),
    tweet("Zombie threads popping up", "Community fears getting bit", -25),        
        #23
    tweet("Clown on the loose!", "Police say 'catching the clown' poses issues", -50),
    tweet("Uncertinty in markets", "questions if yoyocoin actually has value", -200),
        #24
    tweet("Clown on the loose!", "Police say 'catching the clown' poses issues", -50),
    tweet("Uncertinty in markets", "questions if yoyocoin actually has value", -200),
        #25
    tweet("yoyocoin nabs new investors", "Financial future seems bright", 75),
    tweet("Other markets on the rise", "Yoyocoin based economy doing well", 40),
        #26
    tweet("Is anything real?", "Newscaster faces mid-life crisis", -5),
    tweet("Eagle-eyed investor spots repeat headlines", "Questions if news trustworthy", -50),
        #27
    tweet("Ouya two announced", "YoYocoins proud sponsor", -75),
    tweet("Gambling hits forums", "Underaged members enthralled", -50),
        #28
    tweet("Ouya two announced", "YoYocoins proud sponsor", -75),
    tweet("Gambling hits forums", "Underaged members enthralled", -72),
        #29
    tweet("Giant peak incoming", "Prices going up, up, up!", 103),
    tweet("yoyocoin doing fine", "Organization says 'nothing interesting going on'", 4),
        #30
    tweet("Yoyogames buys Simtendo", "Ledgend of Dan maker incoming", 400),
    tweet("Simtendo backs out of deal", "Says other news greatly overblown", -60),
        #31
    tweet("Investor calculates expected growth", "'Yoyocoin increases about $50 every 40 hours, others a tenth of that' claims european toolmaker", 50),
    tweet("Bad news", "Selling now probably wise", -25),
        #32
    tweet("Frequent fluctuations worry investors", "'What other share jumps so dramatically every time a headline is released?' says analyst", -250),
    tweet("Friendly Koopa plays video games", "Simtendo claim unaware of mascot's dealings with yoyocoin", -25),
        #33
    tweet("Lack of sleep plagues jammers", "'My wife will kill me if I don't go to bed' says entrant ", -40),
    tweet("Italian brothers strike again", "'I thought they were just ordinary brothers!' says local on scene", -10),
        #34
    tweet("Unusually many bombs this time around", "Reviewers afraid for life and limb", -20),
    tweet("Mushroom dazzles crowd", "Are green caps the hit new summer trend?", 30),
        #35
    tweet("Bread avoids questioning about secret", "says that pastries and baked good have right to privacy ", 10),
    tweet("Green men in pursuit", "claim nothing is working right ", -10),
        #36
    tweet("Local man goes on hike", "Says weather dreadful, but otherwise a lovely time", 5),
    tweet("Scandal: Insider trading discovered", "investors acting on information from early votes", -75),
        #37
    tweet("GOOD NEWS EVERYBODY!", "You will all be going to deliver a package to the happy cowboy planet!", 50),
    tweet("GOOD NEWS EVERYBODY!", "You will all be going to deliver a package to the deep pit of financial ruin", -50),
        #38
    tweet("Video game market thriving", "Cases of pump and dump found to be overblown. 'All just fake money' says expert", 100),
    tweet("YoYoCoin stagnates", "Sparse market engagement worries key players", -50),
        #39
    tweet("Is anyone listening?", "I am so alone", -25),
    tweet("BULL MARKET!", "Unknown forces driving prices up.", 55),
]



class Command(BaseCommand):
    help = 'Updates the YoYocoin base value'

    def handle(self, *args, **options):
        first = tweet("YoYoCoin launched!","After a rocky development period, yoyocoin is now avaliable for purchase!", 300)
        last = tweet("GMC Jam #41 a roaring success","You can all be proud of yourself, both if you entered or are just playing games", 500)
        now = datetime.datetime(2021, 5, 31, 9, 00)
        stop = datetime.datetime(2021, 6, 14, 7, 00)
        
        t0 = Tweet()
        t0.time = now
        t0.title = first["title"]
        t0.clip = first["clip"]
        t0.valueChange = first["valueChange"]
        t0.save()

        t1 = Tweet()
        t1.time = datetime.datetime(2021, 6, 14, 8, 30)
        t1.title = last["title"]
        t1.clip = last["clip"]
        t1.valueChange = last["valueChange"]
        t1.save()  
        global tweets
        random.shuffle(tweets)
        i = 0
        while now < stop:
            delta = datetime.timedelta(minutes=random.randrange(10, 95))
            now = now + delta 
            chirp = tweets[i]
            t = Tweet()
            t.time = now
            t.title = chirp["title"]
            t.clip = chirp["clip"]
            t.valueChange = chirp["valueChange"]
            t.save()
            i = i + 1
            if(len(tweets) <= i):
                random.shuffle(tweets)
                i = 0
        tweets = Tweet.objects.all()
        print(len(tweets))
            