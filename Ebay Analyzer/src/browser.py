import config as constants
from selenium import webdriver

# gets input and gives suggestions
def openBrowser(windowed = True):
    return webdriver.Firefox() if windowed else webdriver.PhantomJS(constants.PHANTOMPATH)

def openToPage(w, page = constants.BASEURL):
    print("Opening page " + page)
    w.get(page)

def getRelated(w, query):
    print("Searching for " + query)
    w.find_element_by_xpath(constants.SEARCHBOXPATH).send_keys(query)
    w.find_element_by_id(constants.SEARCHSUBMIT_ID).click()
    print("Getting related search")
    return w.find_elements_by_xpath(constants.RELATEDPATH)