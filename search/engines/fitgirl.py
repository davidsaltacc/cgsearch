from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_fitgirl(name):
    
    data = requests.get("https://fitgirl-repacks.site/?s=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    posts = soup.find_all("article", class_="post")

    name_link = []
    for post in posts:
        category_link = post.select_one("header.entry-header div.entry-meta span.cat-links a")
        if category_link and "lossless-repack" in category_link['href']:
            title_link = post.select_one("header.entry-header h1.entry-title a")
            if title_link:
                name_link.append([title_link.get_text(), title_link['href']])
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])
    
    for pair_ in name_link_filtered:

        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://fitgirl-repacks.site/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")
    
        filtered = ["jdownloader2", "internetdownloadmanager", # download managers
                    "nexusmods", "mixmods", "libertycity"] # mods
        
        for li in soup.select("article.post ul li"):
            a_tags = li.find_all("a")

            for a in a_tags:
                valid = True
                
                parent = a.parent 
                if parent and parent.get("class"):
                    classes = parent.get("class")
                    if any("spoiler" in c.lower() for c in (classes if isinstance(classes, list) else [classes])):
                        continue

                href = a.get("href", "")

                if any(f.lower() in href.lower() for f in filtered):
                    valid = False

                if valid:
                    name_lower = a.get_text(strip = True).lower()
                    ltype = "Unsure"
                    if "filehost" in name_lower:
                        ltype = "Direct"
                    elif "rutor" in name_lower or "1337x" in name_lower or "magnet" in name_lower or "torrent" in name_lower or "tapochek" in name_lower or "kat" in name_lower:
                        ltype = "Torrent"

                    yield {
                        "RepackTitle": pair[0],
                        "LinkName": a.get_text(strip = True),
                        "LinkUrl": absolutify_url(href, newUrl),
                        "LinkType": ltype,
                        "RepackPage": newUrl,
                        "Score": score
                    }

generator = get_links_fitgirl
engine_meta = {
    "id": "fitgirl",
    "name": "FitGirl",
    "homepage": "https://fitgirl-repacks.site/",
    "description": "FitGirl is one of the most popular game piracy sites, trusted by many. Contains a lot of games, fast direct file hosts aswell as torrent options."
}