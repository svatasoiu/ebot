'''
Created on Aug 5, 2014

@author: svatasoiu
'''
import item
import config as constants
from selenium.webdriver.support.ui import WebDriverWait

def check(w, ID):
    element = WebDriverWait(w, 10).until(lambda dr: dr.find_element_by_id(ID))
    if not element.is_selected():
        element.click()

def clickPPL(driver):
    try:
        driver.find_element_by_xpath("//input[@name='_fcippl' and @value='4']").click()
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
    w.find_element_by_id("viewType").click()
    WebDriverWait(w, 10).until(clickCustom)
    
    #WebDriverWait(w, 10).until(clickPPL)
    for i in ["7","9","12","13","15"]:
        check(w, "e1-" + i)
    w.find_element_by_id("e1-3").click()

def retrieveAllSimilarItems(w):
    items = w.find_elements_by_xpath(constants.ITEMPATH)
    return [item.Item(i) for i in items]

def filterItems(items):
    pass