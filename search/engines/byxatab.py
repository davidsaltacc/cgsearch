from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_byxatab(name):
    
    data = requests.get("https://byxatab.com/search/" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True), a["href"])
        for a in soup.select("#dle-content .entry .entry__title.h2 a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://byxatab.com/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        # originally says "СКАЧАТЬ ТОРРЕНТ". parsing it is a pain though (it strips the spaces, and if you tell it not to it includes unnecessary characters at the end, including a \xa0), and it doesn't change for any game afaik, so we just hardcode the translation
        torrentLink = [ "DOWNLOAD TORRENT", soup.select_one("#download a.download-torrent")["href"], "Torrent" ]

        yield {
            "RepackTitle": pair[0],
            "DownloadLinks": [ torrentLink ],
            "Score": score
        }

generator = get_links_byxatab
engine_meta = {
    "id": "byxatab",
    "name": "ByXatab",
    "description": "https://byxatab.com/ is a game piracy site trusted by fmhy and others, containing several repacks. Does not feature direct downloads, only torrents."
}