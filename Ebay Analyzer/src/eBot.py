import browser, researcher, analyzer, statistics

# setting up browser
w = browser.openBrowser()
browser.openToPage(w)
browser.getRelated(w, "nexus 7 house")
researcher.setupCustomSearch(w)

# get items
items = researcher.retrieveAllSimilarItems(w)

# analyze and report on items
prices = analyzer.getExistingPrices(items)
analyzer.plotPriceHistogram(items)
(avg, count) = (statistics.mean(prices), len(prices))
print("{:d} items at an average price of ${:.2f}".format(count, avg))

# close
w.close()