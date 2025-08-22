from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_atopgames(name):
    
    data = requests.get("https://atopgames.com/?s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True), a["href"])
        for a in soup.select("ul#posts-container li.post-item .post-details h2 a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://atopgames.com/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        for button in soup.select("a.shortc-button.small.blue"):

            yield {
                "RepackTitle": pair[0],
                "LinkName": button.get_text(strip = True),
                "LinkUrl": absolutify_url(button["href"], newUrl),
                "LinkType": "Direct",
                "RepackPage": newUrl,
                "Score": score
            }

generator = get_links_atopgames
engine_meta = {
    "id": "atopgames",
    "name": "AtopGames",
    "homepage": "https://atopgames.com/",
    "description": "AtopGames is a smaller site hosting several games from different sources on different filehosts."
}