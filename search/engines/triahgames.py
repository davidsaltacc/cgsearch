from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_triahgames(name):
    
    data = requests.get("https://triahgames.com/?s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True).replace("\xa0", " "), a["href"])
        for a in soup.select("div#main .penci-grid li article .grid-header-box h2.entry-title a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://triahgames.com/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        version = None
        
        for strong in soup.select(".wp-block-group__inner-container p strong"):
            print(strong.decode_contents())
            for line in strong.decode_contents().split("<br/>"):
                if line.startswith("Game Version"):
                    version = line.replace("Game Version: ", "")

        # they technically have a magnet link too, but it seems to show N/A for all that i've seen
        for button in soup.select(".maxbutton"):

            yield {
                "RepackTitle": pair[0] + ((" (" + version + ")") if version else ""),
                "LinkName": button.get_text(strip = True),
                "LinkUrl": button["href"],
                "LinkType": "Direct",
                "RepackPage": newUrl,
                "Score": score
            }

generator = get_links_triahgames
engine_meta = {
    "id": "triahgames",
    "name": "TriahGames",
    "homepage": "https://triahgames.com/",
    "description": "TriahGames is a smaller website containing over 1000 different games hosted on multiple filehosts." 
}