from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_appnetica(name):
    
    data = requests.get("https://appnetica.com/search?term=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.select_one("div.font-medium").get_text(strip = True), a["href"])
        for a in soup.select("main#app-content div.space-y-4 div[class=\"\"] a")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]

        name = pair[0]
        
        new_url = absolutify_url(pair[1], "https://appnetica.com/search/")
        data = requests.get(new_url).text
    
        soup = BeautifulSoup(data, "html.parser")

        version = ""

        stats = soup.select("main#app-content .grid .order-first .sticky dl.text-base div")
        for stat in stats:
            if not stat.select_one("dt") == None and stat.select_one("dt").get_text(strip = True).lower() == "версия": # "Version"
                version = stat.select_one("dd button").get_text(strip = True)

        button = soup.select_one("main#app-content .grid .order-first .w-full.border a")

        download_url = absolutify_url(button["href"], "https://appnetica.com/search/")
        link_name = button.get_text().replace("\t", "").replace("\n", "").strip()

        response = requests.get(download_url, allow_redirects = False, stream = True)
        
        if response.status_code in (301, 302, 303, 307, 308):
            download_url = response.headers.get("Location")
        
        response.close()
        
        link_type = "Torrent" if download_url.endswith(".torrent") else "Direct"

        yield {
            "RepackTitle": name + " " + version,
            "LinkName": link_name,
            "LinkUrl": download_url,
            "LinkType": link_type,
            "Score": score
        }

generator = get_links_appnetica
engine_meta = {
    "id": "appnetica",
    "name": "AppNetica",
    "homepage": "https://appnetica.com/",
    "description": "AppNetica is a russian game piracy site containing games for multiple platforms providing direct download. We only search for windows downloads - for some reason most games just say \"Download Unavailable\" for other platforms - so we don't bother searching for it. If someones wants to add that functionality, you are more than welcome to."
}