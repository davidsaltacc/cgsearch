from bs4 import BeautifulSoup
from helpers import filter_matches
import urllib.parse
import requests

def get_links_rexagames(name):
    
    data = requests.get("https://rexagames.com/search/?&quick=1&search_in=titles&start_after=any&updated_after=any&q=" + urllib.parse.quote(name)).text
    # do NOT use quote_plus, it doesn't parse +'ses correctly
    
    soup = BeautifulSoup(data, "html.parser")

    all_results = []

    for post in soup.select("#elSearch_main .ipsBox .ipsStream li.ipsStreamItem"):
        if post.select_one(".ipsStreamItem__mainCell .ipsStreamItem__header .ipsStreamItem__summary span")["title"].lower() == "file":

            a = post.select_one(".ipsStreamItem__mainCell .ipsStreamItem__header .ipsStreamItem__title h2 a")

            title = a.getText(strip = True) + " " + post.select_one(".ipsStreamItem__mainCell .ipsStreamItem__content .ipsStreamItem__content-content .ipsList .i-color_soft").getText(strip = True)
            url = a["href"]

            all_results.append([title, url])
    
    all_results_filtered = filter_matches(name, all_results, itemname_function = lambda x: x[0])

    results = []

    for pair_ in all_results_filtered:

        pair = pair_[0]
        score = pair_[1]
        name = pair[0]
        url = pair[1]

        session = requests.Session() # some links require a cookie to be set
        
        data = session.get(url).text
    
        soup = BeautifulSoup(data, "html.parser")

        link = soup.select_one(".ipsBox--downloadsFile .ipsColumns .ipsButtons a.ipsButton--primary")["href"]

        response = session.get(link, allow_redirects = False)

        # if we didn't do this, users would get hit with a "nuh uh" due to a missing or invalid cookie that only we have here
        if response.status_code in (301, 302, 303, 307, 308):
            link = response.headers.get("Location")

        results.append({
            "RepackTitle": name,
            "Provider": "RexaGames",
            "DownloadLinks": [
                ["Download this file", link, "Direct"] # hardcode title to save effort
            ],
            "Score": score
        })

    return results