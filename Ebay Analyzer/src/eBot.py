#! /usr/bin/python2.6

import browser, researcher, analyzer, sys
import config as constants
from time import time

start = time()
ti = start
# setting up browser
w = browser.openBrowser(windowed=False)
browser.openToPage(w)

search_term = sys.argv[1] if len(sys.argv) > 1 else constants.DEFAULT_SEARCH
browser.getRelated(w, search_term)
researcher.setupCustomSearch(w)
print("Current URL: %s" % w.current_url)

tf = time()
print("Set up took {0:.2f}s".format(tf - ti))
ti = tf

# get items
items = researcher.retrieveAllSimilarItems(w, search_term)
tf = time()
print("Retrieval took {0:.2f}s".format(tf - ti))
ti = tf

# analyze and report on items
analyzer.plotPriceHistograms(items)
analyzer.plotPriceVsTimeLeftGraphs(items)
end = time()

# close
w.close()
print("Total time: {0:.2f}s".format(end - start))
