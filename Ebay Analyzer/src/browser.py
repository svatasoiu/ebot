import config as constants
from selenium import webdriver

# gets input and gives suggestions
def openBrowser(query, windowed = True):
    w = webdriver.Firefox() if windowed else webdriver.PhantomJS(constants.PHANTOMPATH)
    print("Opening window")
    w.get(constants.BASEURL)
    print("Searching for " + query)
    w.find_element_by_xpath(constants.SEARCHBOXPATH).send_keys(query)
    w.find_element_by_id(constants.SEARCHSUBMIT_ID).click()
    print("Getting related search")
    relateds = w.find_elements_by_xpath(constants.RELATEDPATH)
    print(len(relateds))
    for r in relateds:
        print(r.text)
    w.close()
