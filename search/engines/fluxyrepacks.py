from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import requests

def get_links_fluxyrepacks(name):
    
    data = requests.get("https://fluxyrepacks.xyz/games").text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True), a["href"])
        for a in soup.select(".games .game h2 a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0], min_score = 0.85)

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://fluxyrepacks.xyz/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        version = None

        for p in soup.select(".game-detail .game-meta p"):
            if p.select_one("strong") and "version" in p.select_one("strong").get_text(strip = True).lower():
                version = p.get_text(strip = True).replace(p.select_one("strong").get_text(strip = True), "").strip()

        for a in soup.select(".links a.download-link"):
            yield {
                "RepackTitle": pair[0],
                "LinkName": a.get_text(strip = True) + ((" (" + version + ")") if version else ""), # some titles don't include the version, so we add it in the link name to be sure
                "LinkUrl": a["href"],
                "LinkType": "Direct",
                "RepackPage": newUrl,
                "Score": score
            }

generator = get_links_fluxyrepacks
engine_meta = {
    "id": "fluxyrepacks",
    "name": "Fluxy Repacks",
    "homepage": "https://fluxyrepacks.xyz/",
    "description": "Fluxy Repacks is a small site containing about 400 different games hosted as direct downloads on external filehosts."
}