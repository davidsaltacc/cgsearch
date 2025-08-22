from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_reloadedsteam(name):
    
    data = requests.get("https://reloadedsteam.com/?s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.select_one("img")["alt"], a["href"])
        for a in soup.select(".wrap-content .articles-content ul.modern-articles li.single-game > a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://reloadedsteam.com/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        for button in soup.select(".shortc-button.medium.green"):

            yield {
                "RepackTitle": pair[0],
                "LinkName": button.get_text(strip = True),
                "LinkUrl": button["href"],
                "LinkType": "Direct",
                "RepackPage": newUrl,
                "Score": score
            }

generator = get_links_reloadedsteam
engine_meta = {
    "id": "reloadedsteam",
    "name": "Reloaded Steam",
    "homepage": "https://reloadedsteam.com/",
    "description": "Reloaded Steam is a smaller website hosting several games, usually on just one direct download provider."
}