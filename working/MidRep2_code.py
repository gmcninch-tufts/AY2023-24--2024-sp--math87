
import numpy as np
import json

float_formatter = "{:.5f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})

def bv(it,items):
    return np.array([1.0 if i == items.index(it)
                     else 0.0 for i in range(len(items))])

## >>> bv("c",["a","b","c","d"])
## array([0.00000, 0.00000, 1.00000, 0.00000])

def adj_from_json(json_file):
    with open(json_file) as f:
        adj_data = json.load(f)

    dict = {}
    
    for i in adj_data:
        lfrom = i['from']
        lto   = i['to']
        if lfrom in dict.keys():
            dict[lfrom].add(lto)
        else:
            dict[lfrom] = set()
            dict[lfrom].add(lto)
        if not(lto in dict.keys()):
            dict[lto] = set()
            
    sites = list(dict.keys())
    
    A = np.array([sum([bv(l_to,sites) for l_to in dict[l_from]],
                      np.zeros(len(sites)))
                  for l_from in sites]) 
    return (sites, A)
    

#--------------------------------------------------------------------------------

from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from collections import deque, defaultdict
#import datetime
from random import sample

USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0 '
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
              'Apple WebKit/537.36 (KHTML, like Gecko) '
              'Chrome/80.0.3987.149 Safari/537.36')

def unique_url(url):
    """Returns a canonical representation of a link."""
    stripped = url.replace('://www.', '://')
    stripped = stripped.replace(f'{urlparse(url).scheme}://', '').rstrip('/')
    if '#' in stripped:
      # Remove trailing anchor
      return '#'.join(stripped.split('#')[:-1])
    return stripped


def check_page(url):
    """Verifies that a URL corresponds to a reachable web page."""
    try:
        head = requests.head(url,
                             headers={'User-Agent': USER_AGENT},
                             allow_redirects=True,
                             timeout=1)
        content_type = head.headers.get('Content-Type', '').lower()
        return content_type.startswith('text/html')
    except requests.exceptions.RequestException as ex:
        # Couldn't load this particular page, for whatever reason (404, etc.)
        return False


def all_links(url):
    """Retrieves all links from a web page."""
    try:
        req = requests.get(url,
                           headers={'User-Agent': USER_AGENT},
                           allow_redirects=True,
                           timeout=5)
    except requests.exceptions.RequestException as ex:
        # Couldn't load this particular page, for whatever reason (404, etc.)
        return None

    # Get links from page.
    soup = BeautifulSoup(req.text, 'lxml')
    return [link.get('href', '') for link in soup.select('a')]


def filter_links(source_url, urls, blacklist, whitelist,
                 follow_relative_links):
    """Filters and cleans links."""
    filtered = []
    o = urlparse(source_url)
    source_scheme = o.scheme
    source_domain = o.netloc

    for href in urls:
        if not href or href.startswith('#') or \
          (not href.startswith('http') and not follow_relative_links):
            # Only accept absolute links if explicitly allowed;
            # remove empty links and anchors
            continue
        else:
            if href.startswith('//'):
                href = 'https:' + href
            elif href.startswith('/'):
                # Internal link (w.r.t. website root)
                href = f'{source_scheme}://{source_domain}{href}'
            elif not href.startswith('http'):
                # Internal link (w.r.t. current link)
                href = source_url.rstrip('/') + '/' + href
        if '#' in href:
            href = '#'.join(href.split('#')[:-1]) # strip anchor

        # Blacklist/whitelist filtering.
        blacklisted = False
        whitelisted = False
        for keyword in blacklist:
            if keyword.lower() in href.lower():
                blacklisted = True
                break
        for keyword in whitelist:
            if keyword.lower() in href.lower():
                whitelisted = True
                break
        if ((whitelist and whitelisted) or not whitelist) and \
           ((blacklist and not blacklisted) or not blacklist) and \
           'mailto:' not in href and 'javascript:' not in href:
            filtered.append(href)
    return filtered


def crawl(start_url,
          save_file,
          n,
          verbose=True,
          follow_relative_links=True,
          max_links_per_page=float('inf'),
          blacklist=[],
          whitelist=[]):
    """Crawls pages starting from a given URL and saves the link graph.

    :param start_url: The starting URL.
    :param save_file: The JSON file to save crawl data to.
    :param n: The number of pages to add to the graph. Pages in the graph have
        not necessarily been visited (such pages never have outlinks).
    :param verbose: Determines whether to print URLs as they are crawled.
    :param follow_relative_links: Determines whether to follow relative links.
        Following relative links tends to result in narrow, deep crawl--many
        pages being crawled on a relatively small number of websites.
    :param max_links_per_page: The number of links to add to the link queue
        per page. (For each page, the order of links is always shuffled.)
    :param blacklist: A blacklist of URL keywords. If any keyword on the
        blacklist appears in a URL, it will be excluded from the graph and
        not crawled.
    :param whitelist: A whitelist of URL keywords. If the whitelist is nonempty,
        a URL will only be included in the graph and crawled if at least one
        keyword from the whitelist is included in it. The whitelist can be
        combined with the blacklist for highly detailed URL filtering.
    """
    enqueued = set([unique_url(start_url)])
    dead = set([])
    link_graph = []
    link_queue = deque([start_url])
#    ts = datetime.datetime.now().replace(microsecond=0).isoformat()

    while link_queue and len(enqueued) < n:
        # Breadth-first search: the traverse all the links on the first
        # page crawled before moving on to links on the second page crawled,
        # and so on.
        curr_link = link_queue.popleft()
        if verbose:
            print(curr_link)

        # Fetch page metadata and text.
        if not check_page(curr_link):
            # Page not reachable or content type incorrect
            dead.add(curr_link)
            continue
        links = all_links(curr_link)
        if links is None:
            # GET request failed
            dead.add(curr_link)
            continue

        # Filter and sample links from the page.
        # Each filtered link has four possible states:
        # (1) Visited. (The page was loaded and its links were processed.)
        # (2) Dead. (A visit to the page was attempted but failed.)
        # (3) Enqueued. (We intend to eventually visit the page, but we have
        #                not loaded its contents yet.)
        # (4) Unseen. (A page was linked to at some point, but we have not
        #              loaded its contents and do not currently intend to.)
        # Unseen pages are retained in the link graph because we might
        # stumble across them again and decide to visit them after initially 
        # passing them over for visitation. Unseen pages that are not
        # eventually visited are filtered out of the final link graph;
        # dead pages are filtered out as well.
        # Links that pass through states (1) through (3) should be members
        # of the `enqueued` set; this way, they will not be revisited.
        filtered_links = set(filter_links(curr_link,
                                          links,
                                          blacklist,
                                          whitelist,
                                          follow_relative_links=True))
        new_links = [href for href in filtered_links
                     if unique_url(href) not in enqueued]
        sampled_links = sample(new_links,
                               min(max_links_per_page, len(new_links)))
        for link in filtered_links:
            link_graph.append({'from': curr_link, 'to': link})
        for link in sampled_links:
            link_queue.append(link)
            enqueued.add(unique_url(link))

    if verbose:
        print(f'Crawl finished (saw {len(enqueued)} links)')
    filtered = [link for link in link_graph
                if (unique_url(link['to']) in enqueued and 
                   link['to'] not in dead)]
    with open(save_file, 'w') as f:
        json.dump(filtered,f,indent=2)
