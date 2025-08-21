from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_steamrip(name):
    
    data = requests.get("https://steamgg.net/?post_type%5B%5D=portfolio&post_type%5B%5D=post&post_type%5B%5D=page&s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True), a["href"])
        for a in soup.select("#main_wrapper .container .blog-content.wcontainer h2 a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://steamgg.net/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        for a in soup.select(".blog-content .vc_row-flex .wpb_column .wpb_wrapper a.vc_general"):

            yield {
                "RepackTitle": pair[0],
                "LinkName": a.get_text(strip = True),
                "LinkUrl": absolutify_url(a["href"], newUrl),
                "LinkType": "Direct",
                "Score": score
            }

generator = get_links_steamrip
engine_meta = {
    "id": "steamgg",
    "name": "SteamGG",
    "homepage": "https://steamgg.net/",
    "description": "SteamGG is a smaller website hosting over 5000 different games hosted on multiple download providers."
}