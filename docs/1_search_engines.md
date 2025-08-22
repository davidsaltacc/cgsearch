# Custom Search Engines

Firstly, your engine must export two fields - `generator` and `engine_meta`. `engine_meta` simply is a dictionary of metadata about the engine.

**Required Fields in `engine_meta`**

| Name        | Description |
| ----------- | ----------- |
| `id`          | The ID of the search engine, usually all lowercase without any special characters. Is only used internally in several places. |
| `name`        | The friendly name of the engine that users will see. |
| `homepage`    | A link to the repackers/uploaders/distributor's homepage. Will be opened on request of the user. |
| `description` | A short description about the repackers/uploaders/distributor. |

`generator` is a function, more specifically a generator, that yields results based on an input. The function should accept exactly one parameter, that usually being `name` - you can also call it `query` or whatever you like to call it. The generator returns nothing, but yields several results, one for each download link - these results are simple dictionaries with multiple fields. How it gets these results is up to the engine itself. 

**Required Fields in engine result**

| Name        | Description |
| ----------- | ----------- |
| `RepackTitle` | The title of the repack/upload. |
| `RepackPage` | The uploader's page on the repack/upload. |
| `LinkName` | The label or name of the download link. |
| `LinkUrl` | The url of the download link. |
| `LinkType` | Should either be `Direct` for direct downloads, `Torrent` for torrent downloads, `Unsure` if its not sure which one it is, or `Official` for links to official game distribution websites, like steam. |
| `Score` | A score on how accurate to the query this result is. Range is 0-1. How to obtain such a value easily is discussed below. |

### Example flow of a generator function

***Please note that based on what website you create an engine for, this process may be partly or entirely different. This example is oriented on the engine for steam, and this general flow works for a lot of pages, but not for all. You may want to check out existing engines for different flows.***

**1. Get the HTML based on the search query**

You can use `requests.get()` along with `urrlib.parse.quote_plus()` to fetch webpages - like this, for example:

```python
data = requests.get("https://example.site/search?q=" + urllib.parse.quote_plus(query)).text
```
Most websites will then return a page with several search results. Note that in some rare cases, you may need to switch out `quote_plus` for `quote`, as some websites don't parse `+` correctly. Believe me, the first time I encountered that, that was a nightmare to debug.

**2. Create a BeautifulSoup to filter through the html**

```python
soup = BeautifulSoup(data, "html.parser")
```
You may also use different libraries or parsers, but this should work in most scenarios without issue.

**3. Create a list of name-link pairs**

```python
name_link = [
    (a.select_one("div.responsive_search_name_combined .col span.title").get_text(strip = True), a["href"])
    for a in soup.select("div#search_resultsRows a.search_result_row")
]
```

This example works for steam, specifically. The list comprehension creates a pair for each `<a>` element inside a `<div id="search_resultsRows">`. Again, this works on steam, but you may have to rewrite all this logic based on what website you are creating an engine for.

Each pair in the list consists of a name and a link - the name is simply the name of the repack, and the link is a (sometimes relative) link to the repack page.

**4. Most imporantly, filtering**

This is a step that should happen in pretty much every engine, as it not only filters out the bullshit results from the relevant ones, but also provides the score used in the result.

```python
name_link_filtered = filter_matches(query, name_link, itemname_function = lambda x: x[0])
```

`filter_matches` is impored from the `helpers` package. It filters out irrelevant results and assigns each result a score, using the `rapidfuzz` library. The first argument is the actual query that was originally searched for. The second one can be any kind of collection. By default, it assumes it is a simple list of strings. If it is instead a list of pairs, supply `itemname_function`. This function simply tells `filter_matches` how to get the name from an item in the collection passed to it. In our case, the name is stored in the first half of the pair, so we just tell it to get the first element with `x[0]`.

It doesn't return the original collection, it only returns the ones that pass the threshold (which can be configured with `min_score = xyz`, by the way), which is 0.65 by default, and the new collection is a collection of pairs - there pairs are not to be confused with the old ones, these are structured like `(item, score)` - item being the original item from the collection passed to it, and score being the score assigned to it.

**5. Going over each result**

```python
for _pair in name_link_filtered:

    pair = _pair[0]
    score = _pair[1]

    name = pair[0]
    newLink = pair[1]
```

Here, `_pair` is the item-score pair, and `pair` is the actual name-link pair.

**6. Getting the links from each page**

Inside the above loop, you can fetch each new link, and extract all download links from it.

```python
    data = requests.get(newLink).text
    soup = BeautifulSoup(data, "html.parser")
```
Depending on the site, extracting download links may be different. 

**7. Yielding results**

After extracting all download links, you have to yield results.

```python
    for download_link in all_direct_download_links:

        yield {
            ...
        }
```

The structure for the yielded result is provided above. Following the example we already have, assuming `download_link` is an `<a>` element (in bs4), you can do something like this:

```python
{
    "RepackTitle": name,
    "RepackPage": newLink,
    "LinkName": download_link.get_text(strip = True),
    "LinkUrl": download_link["href"],
    "LinkType": "Direct",
    "Score": score
}
```

Here, `LinkType` is hardcoded, as a lot of sites only host one type of download - depending on the site, you may have to dynamically figure out the type.

### Registering your own engine

In `main.py`, you have to import your engine, adding it to the list of existing engine imports, and then you need to add the engine to the `all_engines` list. Then, if everything is done correctly, it should show up in search results. 