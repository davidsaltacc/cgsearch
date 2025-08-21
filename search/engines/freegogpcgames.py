from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests
import base64

def get_links_freegogpcgames(name):
    
    data = requests.get("https://freegogpcgames.com/?s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True), a["href"])
        for a in soup.select("main#main .generate-columns-container article .inside-article .entry-header .entry-title a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://freegogpcgames.com/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        for a in soup.select("a.download-btn"):
            yield {
                "RepackTitle": pair[0],
                "LinkName": a.get_text(strip = True),
                "LinkUrl": base64.b64decode(urllib.parse.parse_qs(urllib.parse.urlparse(a["href"]).query)["url"][0]).decode(), 
                "LinkType": "Torrent", # only torrents
                "RepackPage": newUrl,
                "Score": score
            }

generator = get_links_freegogpcgames
engine_meta = {
    "id": "freegogpcgames",
    "name": "Free GOG PC Games",
    "homepage": "https://freegogpcgames.com/",
    "description": "Free GOG PC Games is a website hosting several GOG games exclusively as torrents. They not only host the latest version, but also older versions of games."
}