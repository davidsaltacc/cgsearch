from helpers import filter_matches
import urllib.parse
import requests
import json

def get_links_steam(name):
    
    data = json.loads(requests.get("https://catalog.gog.com/v1/catalog?order=desc:score&productType=in:game&locale=en-US&query=like:" + urllib.parse.quote_plus(name)).text)
    
    name_link = [
        [game["title"], game["storeLink"]]
        for game in data["products"]
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = pair[1]

        yield {
            "RepackTitle": pair[0],
            "LinkName": "Get on GOG",
            "LinkUrl": newUrl,
            "LinkType": "Official",
            "RepackPage": newUrl,
            "Score": score
        }


generator = get_links_steam
engine_meta = {
    "id": "gog",
    "name": "GOG",
    "homepage": "https://www.gog.com/",
    "description": "GOG is a website selling DRM-free games, respecting that the people want to OWN the game, not just buy it. (If buying isn't owning, then pirating isn't stealing - Probably not Sun Tzu)"
}