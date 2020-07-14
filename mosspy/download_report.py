from threading import Thread
import logging
import os
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

def process_url(url, urls, base_url, path, on_read):
    from bs4 import BeautifulSoup # Backward compability, don't break Moss when bs4 not available.

    logging.debug ("Processing URL: " + url)
    response = urlopen(url)
    html = response.read()
    on_read(url)
    soup = BeautifulSoup(html, 'lxml')
    file_name = os.path.basename(url)

    if not file_name or len(file_name.split(".")) == 1: # Not file name eg. 123456789 or is None
        file_name = "index.html"

    for more_url in soup.find_all(['a', 'frame']):
        if more_url.has_attr('href'):
            link = more_url.get('href')
        else:
            link = more_url.get('src')

        if link and (link.find("match") != -1): # Download only results urls
            link_fragments = link.split('#')
            link = link_fragments[0]  # remove fragment from url
            
            link_hash = ""
            if len(link_fragments) > 1:
                link_hash = "#" + link_fragments[1]
            
            basename = os.path.basename(link)

            if basename == link: # Handling relative urls
                link = base_url + basename

            if more_url.name == "a":
                more_url['href'] = basename + link_hash
            elif more_url.name == "frame":
                more_url['src'] = basename

            if link not in urls:                    
                urls.append(link)

    f = open(os.path.join(path, file_name), 'wb')
    f.write(soup.encode(soup.original_encoding))
    f.close()

def download_report(url, path, connections = 4, log_level=logging.DEBUG, on_read=lambda url: None):
    logging.basicConfig(level=log_level)

    if len(url) == 0:
        raise Exception("Empty url supplied")

    if not os.path.exists(path):
        os.makedirs(path)
    
    base_url = url + "/"
    urls = [url]
    threads = []

    logging.debug("="*80)
    logging.debug("Downloading Moss Report - URL: " + url) 
    logging.debug("="*80)

    # Handling thread
    for url in urls:
        t = Thread(target=process_url, args=[url, urls, base_url, path, on_read])
        t.start()
        threads.append(t)

        if len(threads) == connections or len(urls) < connections:
            for thread in threads:
                thread.join()
                threads.remove(thread)
                break

    logging.debug("Waiting for all threads to complete")
    for thread in threads:
        thread.join()
