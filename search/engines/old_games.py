from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_old_games(name): 
    
    data = requests.get("https://www.old-games.ru/catalog/?gamename=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = False), a["href"]) 
        for a in soup.select("main#main .main-content .listtable tr td table tr td[align=\"left\"] a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://www.old-games.ru/")

        yield {
            "RepackTitle": pair[0],
            "LinkName": "Download from Old-Games.RU",
            "LinkUrl": newUrl.replace("/game/", "/game/download/"),
            "LinkType": "Direct",
            "RepackPage": newUrl,
            "Score": score
        }

generator = get_links_old_games
engine_meta = {
    "id": "old_games",
    "name": "Old-Games.RU",
    "homepage": "https://www.old-games.ru/",
    "description": "Old-Games.RU is a russian website hosting several old games."
}