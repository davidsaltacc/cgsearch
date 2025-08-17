from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_steamrip(name):
    
    data = requests.get("https://steamrip.com/?s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True), a["href"])
        for a in soup.select("#media-page-layout #masonry-grid .thumb-overlay .thumb-content .thumb-title a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://steamrip.com/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        all_link_pairs = []

        for button in soup.select(".entry-content p a.shortc-button.medium"):
            
            if "download" not in button.decode_contents().lower() or "torrent" not in button.decode_contents().lower():
                continue

            parent_text = button.parent.get_text("\n", strip = True).split("\n")[0]

            all_link_pairs.append([parent_text, absolutify_url(button.get("href", ""), newUrl), "Torrent" if "torrent" in button.decode_contents().lower() else "Direct"])

        yield {
            "RepackTitle": pair[0],
            "DownloadLinks": all_link_pairs,
            "Score": score
        }

generator = get_links_steamrip
engine_meta = {
    "id": "steamrip",
    "name": "SteamRIP",
    "description": "https://steamrip.com/ is one of the bigger piracy sites, providing direct downloads to pre-installed games (no installer)."
}