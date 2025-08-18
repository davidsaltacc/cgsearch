import json
import sys
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
import engines.appnetica
import engines.gload

if __name__ != "__main__":
    exit(0)

if len(sys.argv) <= 1:
    exit(0)
else:
    if not sys.argv[1] == "CGSearch" and not sys.argv[1] == "Debug":
        exit(0)

# adjusting this order will also change the order they show up in the ui (as the secondary sort criteria after what is selected)
# - maybe. idk. sometimes the order just feels random as fuck
all_engines = [
    engines.fitgirl, 
    engines.steamrip,
    engines.gamebounty, 
    engines.gload,
    engines.ankergames, 
    engines.rexagames,
    engines.appnetica,
    engines.steamunderground, 
    engines.byxatab, 
    engines.elamigos
]

if sys.argv[1] == "Debug":

    from pprint import pprint

    query = input("Query? ")
    engine = input("Engine? ")

    for eng_ in all_engines:
        if engine in eng_.engine_meta["id"]:
            pprint(list(eng_.generator(query)))
            exit(0)
    
    exit(0)

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
# TODO https://g4u.to/ maybe?
# TODO https://gamesdrive.net/ maybe? maybe also filter out updates, some are updates some are full releases i think
# TODO https://www.myabandonware.com/ maybe? (filter out the ones that don't provide a download link but show a purchase button instead)
# TODO https://www.old-games.ru/ maybe?
# TODO https://rlsbb.ru/ maybe?
# TODO https://scnlog.me/games/?s=TERM is eh, but still maybe maybe maybe
# TODO https://oldgamesdownload.com/?s=TERM maybe? maybe
