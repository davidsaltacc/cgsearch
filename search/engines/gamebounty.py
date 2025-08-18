from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import requests
import json

def get_links_gamebounty(name):
    
    data = requests.get("https://gamebounty.world/").text
    
    soup = BeautifulSoup(data, "html.parser")
    
    all_results = json.loads(soup.select_one("#__NEXT_DATA__").encode_contents())["props"]["pageProps"]["initialGames"]

    # their search engine requires javascript, better to just filter manually
    all_results_filtered = filter_matches(name, all_results, itemname_function = lambda x: x["Title"], min_score = 0.85) 

    for pair_ in all_results_filtered:
        
        data = pair_[0]
        score = pair_[1]

        title = data["Title"] + " " + data["version"] 
        
        link = "https://gamebounty.world/download/" + data["Slug"]

        data = requests.get(link).text
    
        soup = BeautifulSoup(data, "html.parser")

        cc_info = json.loads(soup.select_one("#__NEXT_DATA__").encode_contents())["props"]["pageProps"].get("customContainerInfo")
        if not cc_info:
            continue

        all_mirrors = cc_info.get("mirrors")
        if not all_mirrors:
            continue

        multiple_parts = False

        for mirror in all_mirrors:

            if len(mirror["links"]) == 1:
                yield {
                    "RepackTitle": title,
                    "LinkName": mirror["name"],
                    "LinkUrl": mirror["links"][0]["url"],
                    "LinkType": "Direct",
                    "Score": score
                }
            else:
                multiple_parts = True

        if multiple_parts:
            yield {
                "RepackTitle": title,
                "LinkName": "Download Game (multiple hosts)", # originally just says "Download Game"
                "LinkUrl": link,
                "LinkType": "Direct",
                "Score": score
            }

generator = get_links_gamebounty
engine_meta = {
    "id": "gamebounty",
    "name": "GameBounty",
    "homepage": "https://gamebounty.world/",
    "description": "GameBounty is a game piracy site trusted by fmhy, contains several games. Contains direct downloads hosted on external filehosts only."
}

# okay let me tell you a story
# i reverse engineered what their webpacked code does exactly to load all the games
# very early, i found a huge chunk of json data containing all the games, but they didn't have any link, only an id
# so i reverse engineered everything, trying to figure out how they get an url from the id
# after all that, well, lets just say i now know quite a bit more about reverse engineering webpack
# do you want to know what the solution was in the end? 
# yeah, none of that which i tried to find.
# in the json blob, each game also contains a "slug" - for example, "hollow-knight" for Hollow Knight (the game).
# yeah all you have to do is go to /(slug). god im a fucking idiot

