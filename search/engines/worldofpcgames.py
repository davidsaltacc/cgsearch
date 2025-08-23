from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_worldofpcgames(name):
    
    data = requests.get("https://worldofpcgames.com/?s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.get_text(strip = True), a["href"])
        for a in soup.select(".wrap-content .articles-content ul.modern-articles li .content-list a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://worldofpcgames.com/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        is_game = False

        for category in soup.select(".single-content .entry-top .single-category a"):
            if "game" in category.get_text(strip = False).lower():
                is_game = True
        
        if not is_game:
            continue

        for button in soup.select("center a.enjoy-css"):

            yield {
                "RepackTitle": pair[0],
                "LinkName": button.get_text(strip = True),
                "LinkUrl": button["href"],
                "LinkType": "Direct",
                "RepackPage": newUrl,
                "Score": score
            }

generator = get_links_worldofpcgames
engine_meta = {
    "id": "worldofpcgames",
    "name": "WorldOfPCGames",
    "homepage": "https://worldofpcgames.com/",
    "description": "WorldOfPCGames is a smaller website hosting several games on usually just about one direct download provider."
}