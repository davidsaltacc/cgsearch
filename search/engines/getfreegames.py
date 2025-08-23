from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_getfreegames(name):
    
    data = requests.get("https://getfreegames.net/?s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True), a["href"])
        for a in soup.select("div#main-content .bkmodule .content-wrap ul li .post-c-wrap .title a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://getfreegames.net/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        for button in soup.select(".download-mirrors-container .DownloadButtonContainer a.enjoy-css"):
            
            yield {
                "RepackTitle": pair[0],
                "LinkName": button.get_text(strip = True),
                "LinkUrl": button["href"],
                "LinkType": "Direct",
                "RepackPage": newUrl,
                "Score": score
            }

generator = get_links_getfreegames
engine_meta = {
    "id": "getfreegames",
    "name": "Get Free Games",
    "homepage": "https://getfreegames.net/",
    "description": "Get Free Games is a smaller site hosting several games on direct download providers."
}