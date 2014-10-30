#! /usr/bin/python2.6

import browser, researcher, analyzer
import config as constants
from time import time
from datetime import date
from optparse import OptionParser

# arguments 

parser = OptionParser()
parser.add_option("-s", "--search_term", dest="search_term", default=constants.DEFAULT_SEARCH, help="the term to search for")
parser.add_option("-g", action="store_true", dest="graph", default=False, help="to graph or not to graph")
parser.add_option("-w", action="store_true", dest="windowed", default=False, help="to window or not to window")
parser.add_option("-n", "--max_pages", type=int, dest="max_pages", default=constants.MAXPAGES, help="max number of pages to scrape")
(options, args) = parser.parse_args()

start = time()
ti = start
# setting up browser
w = browser.openBrowser(windowed=options.windowed)
browser.openToPage(w)

search_term = options.search_term
browser.getRelated(w, search_term)
researcher.setupCustomSearch(w)
print("Current URL: %s" % w.current_url)

tf = time()
print("Set up took {0:.2f}s".format(tf - ti))
ti = tf

# get items
with open(constants.LOGFILE % date.today().strftime("%m-%d-%y"), 'a') as logfile:
    items = researcher.retrieveAllSimilarItems(w, options.max_pages, search_term, logfile)
tf = time()
print("Retrieval took {0:.2f}s".format(tf - ti))
ti = tf

# analyze and report on items
if options.graph:
    analyzer.plotPriceHistograms(items)
    analyzer.plotPriceVsTimeLeftGraphs(items)
end = time()

# close
w.close()
print("Total time: {0:.2f}s".format(end - start))
