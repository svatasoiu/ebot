import config as constants
from selenium import webdriver

# gets input and gives suggestions
def openBrowser(windowed = True):
    """ Returns a webdriver with a window or not"""
    return webdriver.Firefox() if windowed else webdriver.PhantomJS(constants.PHANTOMPATH)

def openToPage(w, page = constants.BASEURL):
    """ Opens w to page, with the default specified in config.py """
    print("Opening page " + page)
    w.get(page)

def getRelated(w, query):
    """ Get the suggested related items as determined by Ebay """
    print("Searching for " + query)
    w.find_element_by_xpath(constants.SEARCHBOXPATH).send_keys(query)
    w.find_element_by_id(constants.SEARCHSUBMIT_ID).click()
    print("Getting related search")
    return w.find_elements_by_xpath(constants.RELATEDPATH)
