'''
Created on Aug 5, 2014

@author: svatasoiu
'''
import item
import config as constants
from selenium.webdriver.support.ui import WebDriverWait

def check(w, ID):
    """ makes sure the checkbox with id=ID on w is checked"""
    element = WebDriverWait(w, 10).until(lambda dr: dr.find_element_by_id(ID))
    if not element.is_selected():
        element.click()

def clickPPL(driver):
    try:
        driver.find_element_by_xpath(".//input[@name='_fcippl' and @value='4']").click()
        return True
    except:
        return False

def clickCustom(driver):
    try:
        driver.find_element_by_id("custLink").click()
        return True
    except:
        return False

def setupCustomSearch(w):
    """ Sets up return fields and limits on w """
    w.find_element_by_id("viewType").click()
    WebDriverWait(w, 10).until(clickCustom)
    
    #WebDriverWait(w, 10).until(clickPPL)
    for i in ["7","9","12","13","15"]:
        check(w, "e1-" + i)
    w.find_element_by_id("e1-3").click()

def retrieveAllSimilarItems(w):
    """ Returns all listed items on the current page of w """
    items = w.find_elements_by_xpath(constants.ITEMPATH)
    print("Getting items")
    res = [item.Item(i) for i in items]
    pageNo = 1
    while pageNo < constants.MAXPAGES:
        try:
            print("Next Page...")
            w.find_element_by_xpath(constants.PAGINATIONPATH).click()
            items = w.find_elements_by_xpath(constants.ITEMPATH)
            res += [item.Item(i) for i in items]
            print("Finished with Page")
            pageNo += 1
        except:
            print("Done with Pagination")
            break
    print("Got " + str(len(res)) + " items")
    return res
