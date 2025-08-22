from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_steam(name):
    
    data = requests.get("https://store.steampowered.com/search/?category1=998&term=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.select_one("div.responsive_search_name_combined .col span.title").get_text(strip = True), a["href"])
        for a in soup.select("div#search_resultsRows a.search_result_row")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://store.steampowered.com/search/").split("?")[0]
        
        yield {
            "RepackTitle": pair[0],
            "LinkName": "Get on Steam",
            "LinkUrl": newUrl,
            "LinkType": "Official",
            "RepackPage": newUrl,
            "Score": score 
        }


generator = get_links_steam
engine_meta = {
    "id": "steam",
    "name": "Steam",
    "homepage": "https://store.steampowered.com/",
    "description": "Steam is the biggest game distribution website where you can buy and get most games."
}