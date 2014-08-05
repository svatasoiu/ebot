import browser, researcher

w = browser.openBrowser()
browser.openToPage(w)
browser.getRelated(w, "nexus 7")
researcher.setupCustomSearch(w)
items = researcher.retrieveAllSimilarItems(w)
print(len(items))
for i in items:
    print(i.toString())
w.close()