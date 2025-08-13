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
    
    results = [] 

    for pair_ in all_results_filtered:
        
        data = pair_[0]
        score = pair_[1]

        title = data["Title"] + " " + data["version"] 
        
        link = "https://gamebounty.world/download/" + data["Slug"]

        results.append({
            "RepackTitle": title,
            "Provider": "GameBounty",
            "DownloadLinks": [
                ["Download Game", link, "Direct"] # hardcode title, no need to parse, just saves us effort honestly
            ],
            "Score": score
        })

    return results