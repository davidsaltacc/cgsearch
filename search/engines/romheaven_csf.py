from helpers import filter_matches
import urllib.parse
import requests
import json

def get_links_romheaven_csf(name):
    
    data = json.loads(requests.get("https://6i547qwlncc4kjnhf6mmzs7jvx4nzrxrw4ufv7pq6fvg5gmex7hq.arweave.net/8jvPwstohcUlpy-YzMvprfjcxvG3KFr98PFqbpmEv88").text)
    
    games_filtered = filter_matches(name, data, itemname_function = lambda x: (x["app_name"] + " (Build " + x["build"] + ") (Uncracked - CSF)"), min_score = 0.85)

    for pair_ in games_filtered:

        game = pair_[0]
        score = pair_[1]

        for type in ["pixeldrain", "buzzheavier", "direct"]:
            
            yield {
                "RepackTitle": game["app_name"] + " (Build " + game["build"] + ") (Uncracked - CSF)",
                "LinkName": "Pixeldrain" if type == "pixeldrain" else ("Buzzheavier" if type == "buzzheavier" else "Direct Download"),
                "LinkUrl": "https://pixeldrain.com/u/" + game["pixeldrain"] if type == "pixeldrain" else ("https://buzzheavier.com/f/" + game["buzzheavier"] if type == "buzzheavier" else urllib.parse.quote(f"https://dl.romheaven.com/{game['appid']}.rar?filename=({game['appid']}) {game['install_dir']}.rar")),
                "LinkType": "Direct",
                "RepackPage": "https://romheaven.com/csf",
                "Score": score
            }

generator = get_links_romheaven_csf
engine_meta = {
    "id": "romheaven_csf",
    "name": "RomHeaven CSF",
    "homepage": "https://romheaven.com/csf",
    "description": "RomHeaven is a website that, among other things, provides CSF's (clean, uncracked steam files) for games."
}
