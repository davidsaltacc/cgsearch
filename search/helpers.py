from rapidfuzz import fuzz
import urllib.parse
import sys
import struct

def filter_matches(query, results, min_score = 0.65, itemname_function = lambda x: x):
    query = query.strip()
    filtered = []
    for r in results:
        score = fuzz.partial_ratio(query.lower(), itemname_function(r).lower()) / 100
        if score >= min_score:
            filtered.append((r, score))
    return sorted(filtered, key = lambda x: x[1], reverse = True)

def absolutify_url(href, base_url):
    if href and not href.lower().startswith(("http://", "https://")):
        href = urllib.parse.urljoin(base_url, href)
    return href

def read_message():
    length_bytes = sys.stdin.buffer.read(4)
    if not length_bytes:
        return None
    data = sys.stdin.buffer.read(struct.unpack(">I", length_bytes)[0])
    return (data[:4], data[4:])

def send_message(type: bytes, data: bytes):
    data = type + data
    sys.stdout.buffer.write(struct.pack(">I", len(data)))
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()

def safe_generator(generator, onerror):
    while True:
        try:
            item = next(generator)
        except StopIteration:
            break
        except Exception as e:
            onerror(e)
            continue
        yield item