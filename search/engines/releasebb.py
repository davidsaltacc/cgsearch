from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import urllib.parse
import requests

def get_links_releasebb(name):
    
    data = requests.get("https://rlsbb.ru/?s=" + urllib.parse.quote_plus(name), cookies = {
        "filters": "games,_games_pc,_games_mac-games"
    }).text
    
    soup = BeautifulSoup(data, "html.parser")
    
    name_post = [
        (post.select_one(".entry-header-wrapper header.entry-header h1.entry-title a").get_text(strip = True), post)
        for post in soup.select("div#post-wrapper .post-wrapper-hentry article .post-content-wrapper .entry-data-wrapper")
    ]
    
    name_post_filtered = filter_matches(name, name_post, itemname_function = lambda x: x[0])

    for pair_ in name_post_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        name = pair[0]
        post = pair[1]

        if post.select_one(".entry-summary p em strong a") != None and post.select_one(".entry-summary p em strong a").getText(strip = True) == "changelog.txt":
            continue

        for a in post.select(".entry-summary p")[-1].select("a"):

            yield {
                "RepackTitle": name,
                "LinkName": a.getText(strip = True),
                "LinkUrl": a["href"],
                "LinkType": "Direct",
                "Score": score
            }

generator = get_links_releasebb
engine_meta = {
    "id": "releasebb",
    "name": "ReleaseBB",
    "homepage": "https://rlsbb.ru/",
    "description": "ReleaseBB is a multimedia piracy site not just for games, but also other content. Contains games for windows and other platforms. Mostly only hosts files on slow providers. Allows users to re-upload the files for themselves and post them in the comments - but these most likely cannot be verified to be safe."
}