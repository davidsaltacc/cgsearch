import json
import sys
import struct
import ctypes
import traceback
from threading import Thread
import engines.triahgames
from helpers import read_message, send_message, safe_generator

import filehosts

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
import engines.releasebb
import engines.unioncrax
import engines.freegogpcgames
import engines.fluxyrepacks
import engines.myabandonware
import engines.steamgg
import engines.atopgames
import engines.steam
import engines.gog
import engines.triahgames

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
    engines.steam,
    engines.gog,
    engines.fitgirl, 
    engines.steamrip,
    engines.gamebounty, 
    engines.freegogpcgames, 
    engines.gload,
    engines.ankergames, 
    engines.rexagames,
    engines.fluxyrepacks,
    engines.appnetica,
    engines.unioncrax,
    engines.steamgg,
    engines.steamunderground, 
    engines.triahgames, 
    engines.byxatab,
    engines.atopgames,
    engines.releasebb, 
    engines.elamigos,
    engines.myabandonware
]

if sys.argv[1] == "Debug":

    from pprint import pprint

    query = input("Query? ")
    engine = input("Engine? ")

    for eng_ in all_engines:
        if engine == eng_.engine_meta["id"]:
            pprint(list(eng_.generator(query)))
            exit(0)
    
    exit(0)

boost_official_links = True 
lower_bad_filehosts = True

excluded_engines = []

search_thread = None

try:
    while True:
        msg = read_message()
        if msg[0] is None:
            break
        
        msg_type = msg[0]
        msg_data = msg[1]

        if msg_type == b"srch": # start search

            def start_search():
                query = msg_data.decode()
                send_message(b"rset", b"")

                for engine in all_engines:
                    if engine.engine_meta["id"] in excluded_engines:
                        continue
                        
                    def on_error(e):
                        message = ("search engine " + engine.engine_meta["id"] + " failed: \n" + "".join(traceback.format_exception(e)) + "\n").encode()
                        sys.stderr.buffer.write(struct.pack(">I", len(message)))
                        sys.stderr.buffer.write(message)
                        sys.stderr.buffer.flush()
                    
                    for result in safe_generator(engine.generator(query), on_error):

                        try: # this is the only section that isn't inside a try block otherwise, so we put it manually 
                        
                            if (len(result["LinkUrl"].strip()) == 0):
                                continue
                                
                            if (result["LinkType"] == "Official") and boost_official_links:
                                result["Score"] *= 1.2
                            
                            filehost = filehosts.get_filehost(result["LinkName"], result["LinkType"], result["LinkUrl"])

                            result["Filehost"] = filehost.name
                            # so for some reason, because there was an error being thrown trying to get the filehost, mentioning filehost in any way besides defining it causes my memory usage to spike about 1gb.

                            if lower_bad_filehosts:
                                if filehost.bad == filehosts.IsBad.Yes:
                                    result["Score"] *= 0.6
                                if filehost.bad == filehosts.IsBad.Slightly:
                                    result["Score"] *= 0.9

                            send_message(b"link", json.dumps({ 
                                "engine_id": engine.engine_meta["id"],
                                "result": result
                            }).encode())
                        
                        except Exception as e:
                            on_error(e)
                
                send_message(b"done", b"")
            
            search_thread = Thread(target = start_search)
            search_thread.start()
        
        if msg_type == b"cncl": # cancel
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(search_thread.ident), ctypes.py_object(SystemExit))
            send_message(b"done", b"")
            # KILL IT WITH FIRE!!!!
            # sorry, writing this whole cgsearch thing is making me go insane
            # on a serious note, i don't think there is any drawbacks to just killing it 

        if msg_type == b"egns": # list engines
            data = {}
            for eng in all_engines:
                data[eng.engine_meta["id"]] = eng.engine_meta
            send_message(b"egns", json.dumps(data).encode())

        if msg_type == b"bsof": # boost official links above others
            boost_official_links = msg_data.decode() == "true"
        
        if msg_type == b"lbfh": # lower bad file hosts
            lower_bad_filehosts = msg_data.decode() == "true"
        
        if msg_type == b"lnfo": # get potential warnings about link
            data = {
                "query": msg_data.decode()
            }
            query = json.loads(msg_data.decode())
            result = filehosts.warning_filehost(query[0], query[1], query[2])
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
except Exception as e:
    message = ("critical error in search engine occured: \n" + "".join(traceback.format_exception(e)) + "\n").encode()
    sys.stderr.buffer.write(struct.pack(">I", len(message)))
    sys.stderr.buffer.write(message)
    sys.stderr.buffer.flush()

# TODO https://romheaven.com/csf maybe - add "uncracked" to names, otherwise people may end up confused
# TODO https://gamepcfull.com/?s=QUERY
# TODO https://www.cg-gamespc.com/games?game=QUERY
# TODO https://worldofpcgames.com/?s=QUERY
# TODO https://getfreegames.net/?s=QUERY
# TODO https://reloadedsteam.com/?s=QUERY
# TODO https://elenemigos.com/?g_name=QUERY&platform=PC&order=last_update
# TODO https://www.old-games.ru/ maybe?
# TODO https://oldgamesdownload.com/?s=QUERY maybe? maybe
