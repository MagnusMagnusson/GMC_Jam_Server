# GMC_Jam_Server

A little hobby [Django](https://www.djangoproject.com/) server I use for online capabilities when making games for the [GameMaker Community](https://forum.yoyogames.com/index.php) game jams. None of these are commercial products
and can be freely replicated as you wish. Given each game is made over a four day period do not expect any quality craftmanship here, this is all rushed together
and operates on tape and good will alone. If you decide to play around with this you'll have to deal with all of the contained bugs and shoddy structure yourself. 

# Setting up

1 ) Install a Python3 virtual enviroment (or not, I'm not your boss) and on it Django with all appropriate dependancies. 
2 ) Find all files marked with "_example", remove the _example, and alter the contained settings to something fitting your project. These files may contain sensitive
information or keys and should not be included in source control. 
3 ) Optionally if you do not want to use sqlite install the appropriate drivers, change the setting in gmc/settings.py, and continue from there. 
4 ) Run "python manage.py migrate" to initialize the database. 
5 ) Happy developing!

# Included projects

## Jam_40

A highscore server for "The Crimson Guild's Glamorous Guest List", my entry in to the GMC jam 40. [It has its own repository](https://github.com/MagnusMagnusson/CG_GuestList_Jam40) which
includes an earlier copy of this server. That project is probably broken as I fiddled a bit with it after the jam and didn't finish synchronizing my changes everywhere, so 
chances are it doesn't work. 

## YoYoCoin Market

A fictional stock-market that I submitted to the GMC Jam 41. You'll need to initialize the companies and the news stories and give them some starting value. Currently it updates once per minute via 
a cron job, or by manually calling the "updatePrice" management function. Players are allowed to create account and then use those to buy and sell to their hearts content on the
very exploitable stock market. 
