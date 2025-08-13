from rapidfuzz import fuzz
import urllib.parse

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