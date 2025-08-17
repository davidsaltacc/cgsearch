from bs4 import BeautifulSoup
from helpers import absolutify_url, filter_matches
import requests

def get_links_elamigos(name):
    
    data = requests.get("https://elamigos.site/").text
    
    soup = BeautifulSoup(data, "html.parser")
    
    allRepacks = []

    for a in soup.select("h3 > a"):
        
        if "download" not in a.decode_contents().lower():
            continue

        parent_text_words = a.parent.get_text(strip = True).split(" ")
        if parent_text_words:
            parent_text_words.pop()

        href = absolutify_url(a.get("href", ""), "https://elamigos.site/")

        allRepacks.append([" ".join(parent_text_words), href])
    
    all_results_filtered = filter_matches(name, allRepacks, itemname_function = lambda x: x[0], min_score = 0.85) 
    # most sites have a search engine built in, we only use the low .6 threshold to filter out random bullshit that gets included in the results for some reason
    # elamigos does not have a search engine (unless you count Ctrl+F), so we use a higher threshold to filter out all things unrelated

    for pair_ in all_results_filtered:
        
        pair = pair_[0]
        score = pair_[1]
        
        newUrl = pair[1]
        data = requests.get(newUrl).text
    
        soup = BeautifulSoup(data, "html.parser")

        all_link_pairs = []

        for h2 in soup.select("h2"):
            pairs = []
            el = h2.find_next_sibling()
            while el and el.name == "h3":
                a = el.find("a")
                if not a:
                    break
                href = a.get("href", "")
                pairs.append([h2.get_text(strip = True), href, "Direct"]) # elamigos does not provide torrents, as far as i am aware
                el = el.find_next_sibling()
            all_link_pairs.extend(pairs)
    
        yield {
            "RepackTitle": pair[0],
            "DownloadLinks": all_link_pairs,
            "Score": score
        }

generator = get_links_elamigos
engine_meta = {
    "id": "elamigos",
    "name": "ElAmigos",
    "description": "https://elamigos.site/ is a site with a number of repacks. The repacks are only hosted on slow download providers, so your downloads will take a very long time if you don't pay for the hoster's premium option."
}