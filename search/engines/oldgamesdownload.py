from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_oldgamesdownload(name): 
    
    data = requests.get("https://oldgamesdownload.com/?s=" + urllib.parse.quote_plus(name), headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3"
    }).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True), a["href"]) 
        for a in soup.select("main#main .generate-columns-container article div h3 a")
    ]

    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://oldgamesdownload.com/")

        yield {
            "RepackTitle": pair[0],
            "LinkName": "Download from Old Games Download",
            "LinkUrl": newUrl,
            "LinkType": "Direct",
            "RepackPage": newUrl,
            "Score": score
        }

generator = get_links_oldgamesdownload
engine_meta = {
    "id": "oldgamesdownload",
    "name": "Old Games Download",
    "homepage": "https://oldgamesdownload.com/",
    "description": "Old Games Download is a website hosting old games."
}