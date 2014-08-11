#! /usr/bin/python3.4

import browser, researcher, analyzer, sys
import config as constants
from time import time

start = time()
ti = start
# setting up browser
w = browser.openBrowser(windowed=True)
browser.openToPage(w)
browser.getRelated(w, sys.argv[1] if len(sys.argv) > 1 else constants.DEFAULT_SEARCH)
researcher.setupCustomSearch(w)

tf = time()
print("Set up took {:.2f}s".format(tf - ti))
ti = tf

# get items
items = researcher.retrieveAllSimilarItems(w)
tf = time()
print("Retrieval took {:.2f}s".format(tf - ti))
ti = tf

# analyze and report on items
analyzer.plotPriceHistograms(items)
end = time()

# close
w.close()
print("Total time: {:.2f}s".format(end - start))