import browser, researcher, analyzer
from time import time

start = time()
ti = start
# setting up browser
w = browser.openBrowser(windowed=True)
browser.openToPage(w)
browser.getRelated(w, "nexus 7")
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