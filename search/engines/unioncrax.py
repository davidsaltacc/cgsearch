from helpers import filter_matches
import requests
import json

def get_links_unioncrax(name):
    
    data = json.loads(requests.get("https://be-antwerp-po-db.pages.dev/db.json").text)
    
    name_link = [ (game["name"] + " (" + game["version"] + ")", game["link"], game["size"]) for game in data ] # i know that f-strings are a thing, thank you. 
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0], min_score = 0.85)

    for pair_ in name_link_filtered:
        pair = pair_[0]
        yield {
            "RepackTitle": pair[0],
            "LinkName": "Download (" + pair[2] + ")", # doesn't have a link name, so why not just put the file size in 
            "LinkUrl": pair[1],
            "LinkType": "Direct",
            "Score": pair_[1]
        }

generator = get_links_unioncrax
engine_meta = {
    "id": "unioncrax",
    "name": "UnionCrax",
    "homepage": "https://union-crax.xyz/",
    "description": "UnionCrax is a game piracy site trusted by fmhy, containing about a thousand repacks for several popular games. Features direct downloads on multiple filehosts."
}
