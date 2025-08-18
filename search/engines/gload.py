from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_gload(name):
    
    data = requests.get("https://gload.to/?s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link_rlsname = [
        (a.select_one(".gamemainansichttitel").get_text(strip = True), a["href"], a.select_one(".gamemainansichtrlstitel").get_text(strip = True))
        for a in soup.select("main.tm-content a.titelcontenta")
    ]
    
    name_link_filtered = filter_matches(name, name_link_rlsname, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://gload.to/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        for a in soup.select("div#dldiv a.dlhoster"):

            yield {
                "RepackTitle": pair[2],
                "LinkName": a.select_one("span").get_text(strip = True),
                "LinkUrl": a["href"],
                "LinkType": "Direct",
                "Score": score
            }

generator = get_links_gload
engine_meta = {
    "id": "gload",
    "name": "GLOAD",
    "homepage": "https://gload.to/",
    "description": "GLOAD is a german game piracy site containing different repacks for several games, on multiple platforms, with multiple filehosts per repack."
}