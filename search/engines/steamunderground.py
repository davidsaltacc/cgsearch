from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_steamunderground(name):

    data = requests.get("https://steamunderground.net/?s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")

    name_link = [
        (a.get_text(strip = True), a["href"])
        for a in soup.select("#body-wrapper #main-content .bkmodule ul li h4.title a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    results = [] 

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        data = requests.get(absolutify_url(pair[1], "https://steamunderground.net/")).text
    
        soup = BeautifulSoup(data, "html.parser")

        all_link_pairs = [
            [a.get_text(strip = True), a["href"], "Direct"] # only direct downloads
            for a in soup.select(".download-mirrors-container .DownloadButtonContainer a.enjoy-css")
        ]

        results.append({
            "RepackTitle": pair[0],
            "Provider": "SteamUnderground",
            "DownloadLinks": all_link_pairs,
            "Score": score
        })
        
    return results