import json
from threading import Thread, Event
from helpers import read_message, send_message, safe_generator

import stats.link_warnings

import engines.steamrip 
import engines.fitgirl 
import engines.elamigos 
import engines.byxatab 
import engines.ankergames 
import engines.steamunderground 
import engines.gamebounty 
import engines.rexagames 

if __name__ != "__main__":
    exit(0)

all_engines = [
    engines.steamrip,
    engines.fitgirl, 
    engines.elamigos, 
    engines.byxatab, 
    engines.ankergames, 
    engines.steamunderground, 
    engines.gamebounty, 
    engines.rexagames
]

excluded_engines = []

search_thread = None
cancel = None

while True:
    msg = read_message()
    if msg[0] is None:
        break
    
    msg_type = msg[0]
    msg_data = msg[1]

    if msg_type == b"srch": # start search

        def start_search(cancel_event):
            query = msg_data.decode()
            send_message(b"rset", b"")

            for engine in all_engines:
                if engine.engine_meta["id"] in excluded_engines:
                    continue
                
                for result in safe_generator(engine.generator(query), lambda e: sys.stderr.write("search engine " + engine.engine_meta["id"] + " failed: \n" + repr(e) + "\n")):

                    if cancel_event.is_set():
                        send_message(b"done", b"")
                        return

                    send_message(b"link", json.dumps({ 
                        "engine_id": engine.engine_meta["id"],
                        "result": result
                    }).encode())
            
            send_message(b"done", b"")
        
        cancel = Event()
        search_thread = Thread(target = start_search, args = (cancel,))
        search_thread.start()
    
    if msg_type == b"cncl": # cancel
        cancel.set()

    if msg_type == b"egns": # list engines
        data = {}
        for eng in all_engines:
            data[eng.engine_meta["id"]] = eng.engine_meta
        send_message(b"egns", json.dumps(data).encode())
    
    if msg_type == b"lnfo": # get potential warnings about link
        data = {
            "query": msg_data.decode()
        }
        result = stats.link_warnings.information_filehost(json.loads(msg_data.decode()))
        if result:
            data["message"] = result
        send_message(b"lnfo", json.dumps(data).encode())
    
    if msg_type == b"xegn": # exclude/include engine from search
        data = json.loads(msg_data)
        action = data["action"]
        engine_id = data["id"]
        if action == "exclude" and not engine_id in excluded_engines:
            excluded_engines.append(engine_id)
        if action == "include" and engine_id in excluded_engines:
            excluded_engines.remove(engine_id)

# TODO upload date in data?
# TODO also helper functions for finding data on things such as - descriptions for filehosters (get link url and link name, filter out common filehosts), descriptions for repack providers - either directly force in results, or add only in helper - probably helper though
# TODO a homepage link also attached in results - with the repackers page on this game
# TODO add support for parsing filecrypt.cc and similar sites directly and expanding them into more links
# TODO https://m4ckd0ge-repacks.site/all-repacks.html - doesn't have many repacks, but many filehosts i guess - and may grow in the future? search in the <a>'s href's, i guess - as there is no exact search feature 
# TODO https://appnetica.com/games maybe? (includes a version thing, include that in displayed title!)
# TODO https://g4u.to/ maybe?
# TODO https://gload.to/?s=TERM hell yeah, but include the small title under the game title instead. coz that includes version and platform etc etc
# TODO https://gamesdrive.net/ maybe? maybe also filter out updates, some are updates some are full releases i think
# TODO https://www.myabandonware.com/ maybe? (filter out the ones that don't provide a download link but show a purchase button instead)
# TODO https://www.old-games.ru/ maybe?
# TODO https://rlsbb.ru/ maybe?
# TODO https://scnlog.me/games/?s=TERM is eh, but still maybe maybe maybe
# TODO https://oldgamesdownload.com/?s=TERM maybe? maybe
