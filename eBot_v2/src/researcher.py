'''
Created on Dec 27, 2014

@author: svatasoiu
'''

from lxml import etree
import requests
import threading
import Queue
import config as constants
from item import init_from_html_lxml

def format_for_web(s):
    return s.replace(" ", "%20")

def scrape_page(researcher, url, db_conn, search_term, logfile):
    try:
        response = requests.get(url)
        parser = etree.HTMLParser()
        tree = etree.fromstring(response.text.encode('utf8'), parser)
        itemXMLs = tree.findall(".//ul[@id='ListViewInner']/li")
        for elt in itemXMLs:
            researcher.all_items.append(init_from_html_lxml(elt, db_conn, search_term, logfile))
        print("Got %s items from %s" % (len(itemXMLs), url))
    except Exception as exp:
        print(exp)
    finally:
        researcher.queue.get()
        researcher.queue.task_done()
        researcher.db_pool.close_connection(db_conn)

class Researcher:    
    def __init__(self, url, max_items, search_term="", db_pool=None, logfile=None, queue=None):
        # url should have three format {}, one for s_term, one for page start
        self.search_term = search_term
        self.db_pool = db_pool
        self.logfile = logfile
        self.max_items = max_items
        self.queue = queue if queue else Queue.Queue(maxsize = constants.MAX_THREADS)
        self.start_url = url.format(format_for_web(search_term), "{}", "{}")
        print self.start_url
        self.num_pages = self.get_number_of_pages()
        print self.num_pages
        self.all_items = []
        
    """ starts a bunch of threads, so returns a Queue. 
    Need to join on queue """ 
    def scrape_all_pages(self):
        for page_no in range(self.num_pages):
            url = self.start_url.format(page_no + 1, page_no * constants.ITEMS_PER_PAGE)
            t = threading.Thread(target=scrape_page, args=(self, url, self.db_pool.get_connection(), self.search_term, self.logfile))
            print(self.queue.qsize(), t)
            self.queue.put(t)
            t.start()
        return self.queue
            
    def get_number_of_pages(self):
        response = requests.get(self.start_url.format(0, 0))
        parser = etree.HTMLParser()
        tree = etree.fromstring(response.text.encode('utf8'), parser)
        num_results = int(tree.xpath(constants.NUMRESULTSPATH)[0].split(" ")[0].replace(",",""))
        return min(num_results, self.max_items) / 50 + 1
    