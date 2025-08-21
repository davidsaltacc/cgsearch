from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_ankergames(name):
    
    data = requests.get("https://ankergames.net/search/" + urllib.parse.quote(name)).text
    # do NOT use quote_plus - ankergames does not parse it correctly
    
    soup = BeautifulSoup(data, "html.parser")

    name_link = []

    for div in soup.select("div.custom-container div.group.cursor-pointer"):
        h3 = div.select_one("h3.text-white.font-medium.text-sm")
        a_tag = div.find("a")

        if not h3 or not a_tag:
            continue

        text = h3.get_text(strip = True)
        href = a_tag.get("href", "")

        name_link.append([text, href])

    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://ankergames.net/search/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        version = soup.select_one("div.container span.animate-glow.bg-green-500").getText(strip = True)

        yield {
            "RepackTitle": pair[0] + " " + version,
            "LinkName": "Download",
            "LinkUrl": newUrl,
            "LinkType": "Direct", # they host it directly on their website 
            "RepackPage": newUrl,
            "Score": score
        }

generator = get_links_ankergames
engine_meta = {
    "id": "ankergames",
    "name": "AnkerGames",
    "homepage": "https://ankergames.net",
    "description": "AnkerGames is a piracy site trusted by fmhy, which contains a selection of games. Has fast downloads as the files are not hosted on a slow file hoster."
}