from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_steamrip(name):
    
    data = requests.get("https://www.cg-gamespc.com/games?game=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True), a["href"])
        for a in soup.select(".catalog .container .row--grid .card .card__content .card__title a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://www.cg-gamespc.com/games/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        for button in soup.select(".download_btn"):

            yield {
                "RepackTitle": pair[0],
                "LinkName": button.get_text(strip = True),
                "LinkUrl": button["href"],
                "LinkType": "Torrent" if "torrent" in button.get_text(strip = False).lower() or "magnet" in button.get_text(strip = False).lower() else "Direct",
                "RepackPage": newUrl,
                "Score": score
            }

generator = get_links_steamrip
engine_meta = {
    "id": "cg_gamespc",
    "name": "CG-GamesPC",
    "homepage": "https://www.cg-gamespc.com/",
    "description": "CG-GamesPC is a website hosting several games on multiple direct download filehosts."
}