from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_elenemigos(name):
    
    data = requests.get("https://elenemigos.com/?platform=PC&order=last_update&g_name=" + urllib.parse.quote_plus(name)).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_link = [
        (a.select_one(".p-4 h2.font-bold").get_text(strip = True), a["href"])
        for a in soup.select("main.container .grid a.border")
    ]
    
    name_link_filtered = filter_matches(name, name_link, itemname_function = lambda x: x[0])

    for pair_ in name_link_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = absolutify_url(pair[1], "https://elenemigos.com/")
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        index = 0

        for link_container in soup.select(".container .w-full .p-6 .mb-6"):

            index += 1

            version = soup.select_one("button.w-full span.items-center.text-base").decode_contents().split("</i>")[1]
            
            for filehost in soup.select("#version-dropdown-" + str(index) + " .mb-4"):

                filehost_name = filehost.select_one(".items-center span.text-lg.text-white").get_text(strip = True)

                for adlink in filehost.select(".flex a.block.download-link"):

                    download_url = adlink["href"]

                    adlink_provider = adlink.get_text(strip = True).replace("ADS", "")
                    
                    print(filehost_name, adlink_provider)

                    yield {
                        "RepackTitle": pair[0],
                        "LinkName": filehost_name + " (" + version + ") (" + adlink_provider + ")",
                        "LinkUrl": download_url,
                        "LinkType": "Direct",
                        "RepackPage": newUrl,
                        "Score": score
                    }

generator = get_links_elenemigos
engine_meta = {
    "id": "elenemigos",
    "name": "ElEnemigos",
    "homepage": "https://elenemigos.com/",
    "description": "ElEnemigos is a website hosting several games for multiple platforms on multiple filehosts. Please beware that the downloads are hidden behind several ad challenges."
}
