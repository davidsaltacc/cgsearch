from bs4 import BeautifulSoup
from helpers import filter_matches, absolutify_url
import urllib.parse
import requests

def get_links_myabandonware(name):
    
    data = requests.get("https://www.myabandonware.com/search/q/" + urllib.parse.quote_plus(name)).text

    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        [ a.get_text(strip = True), a["href"] ] 
        for a in soup.select("div#content .games .item a.c-item-game__name")
    ]

    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:

        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://www.myabandonware.com/search/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        if soup.select_one("div#download"):
            yield { 
                "RepackTitle": pair[0], 
                "LinkName": "Download from MyAbandonware",
                "LinkUrl": newUrl + "#download", # several links sometimes, just link the user to the page so they can get what they want
                "LinkType": "Direct",
                "RepackPage": newUrl,
                "Score": score
            }

generator = get_links_myabandonware
engine_meta = {
    "id": "myabandonware",
    "name": "My Abandonware",
    "homepage": "https://www.myabandonware.com/",
    "description": "My Abandonware is a website hosting old abandonware games that cannot be obtained through legitimate means anymore."
}
