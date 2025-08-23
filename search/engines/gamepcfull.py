from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_gamepcfull(name):
    
    data = requests.get("https://gamepcfull.com/?s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True), a["href"])
        for a in soup.select("main#main .posts-wrap article .archive-content .entry-header .entry-title a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://gamepcfull.com/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        for button_container in soup.select(".entry-content div.wp-block-buttons"):
            if "download" in button_container.get_text(strip = False).lower():
                block = button_container.find_next_sibling()
                for a in block.select("p > a"):
                    link = a["href"]
                    link_name = a.parent.find_previous_sibling().select_one("strong").get_text(strip = False).replace("\xa0", " ")[:-1]

                    yield {
                        "RepackTitle": pair[0],
                        "LinkName": link_name,
                        "LinkUrl": link,
                        "LinkType": "Torrent" if "torrent" in link_name.lower() or "magnet" in link_name.lower() else "Direct",
                        "RepackPage": newUrl,
                        "Score": score
                    }

generator = get_links_gamepcfull
engine_meta = {
    "id": "gamepcfull",
    "name": "GamePCFull",
    "homepage": "https://gamepcfull.com/",
    "description": "GamePCFull is a small website hosting several games on multiple direct download providers aswell as torrents."
}