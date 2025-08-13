from pprint import pprint
from engines.steamrip import get_links_steamrip
from engines.fitgirl import get_links_fitgirl
from engines.elamigos import get_links_elamigos
from engines.byxatab import get_links_byxatab
from engines.ankergames import get_links_ankergames
from engines.steamunderground import get_links_steamunderground
from engines.gamebounty import get_links_gamebounty
from engines.rexagames import get_links_rexagames

if __name__ == "__main__":
    pprint(("hollow kn"))
    input()

# TODO a homepage link also attached in results - with the repackers page on this game
# TODO add support for parsing filecrypt.cc and similar sites directly and expanding them into more links
# TODO https://m4ckd0ge-repacks.site/all-repacks.html - doesn't have many repacks, but many filehosts i guess - and may grow in the future? search in the <a>'s href's, i guess - as there is no exact search feature 
# TODO https://appnetica.com/games maybe? (includes a version thing, include that in displayed title!)
# TODO https://g4u.to/ maybe?
# TODO https://gload.to/?s=TERM hell yeah, but include the small title under the game title instead. coz that includes version and platform etc etc
# TODO https://gamesdrive.net/ maybe? maybe also filter out updates, some are updates some are full releases i think
# TODO https://www.myabandonware.com/ maybe? (filter out the ones that don't provide a download link but show a purchase button instead)
# TODO https://www.old-games.ru/ maybe?
# TODO https://rlsbb.ru/ maybe?
# TODO https://scnlog.me/games/?s=TERM is eh, but still maybe maybe maybe
# TODO https://oldgamesdownload.com/?s=TERM maybe? maybe
# okay let me tell you a story
# i reverse engineered what their webpacked code does exactly to load all the games
# very early, i found a huge chunk of json data containing all the games, but they didn't have any link, only an id
# so i reverse engineered everything, trying to figure out how they get an url from the id
# after all that, well, lets just say i now know quite a bit more about reverse engineering webpack
# do you want to know what the solution was in the end? 
# yeah, none of that which i tried to find.
# in the json blob, each game also contains a "slug" - for example, "hollow-knight" for Hollow Knight (the game).
# yeah all you have to do is go to /(slug). god im a fucking idiot

