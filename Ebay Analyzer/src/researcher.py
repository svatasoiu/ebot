'''
Created on Aug 5, 2014

@author: svatasoiu
'''
import item
import config as constants
import db_config as db_constants
import mysql.connector
from datetime import datetime
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

def retrieveAllSimilarItems(w, max_pages, search_term = "", logfile=None):
    """ Returns all listed items on the current page of w """
    db_conn = mysql.connector.connect(**db_constants.DBCONFIG)
    
    items = w.find_elements_by_xpath(constants.ITEMPATH)
    print("Getting items")
    res = [item.Item(i, db_conn, search_term) for i in items]
    pageNo = 1
    while pageNo < max_pages:
        print(pageNo)
        print(max_pages)
        print (pageNo < max_pages)
        try:
            print("Next Page...")
            w.find_element_by_xpath(constants.PAGINATIONPATH).click()
            items = w.find_elements_by_xpath(constants.ITEMPATH)
            res += [item.Item(i, db_conn, search_term) for i in items]
            print("Finished with Page")
            if logfile:
                try:
                    time_now = datetime.now().strftime("%I:%M:%S%p")
                    logfile.write("%s: (term=%s) Finished page of %s items\n" % (time_now, search_term, str(len(items))))
                except:
                    pass
            pageNo += 1
        except:
            print("Done with Pagination")
            break
    print("Got " + str(len(res)) + " items")
    if logfile:
        try:
            time_now = datetime.now().strftime("%I:%M:%S%p")
            logfile.write("%s: (term=%s) Researcher got a total of %s items\n" % (time_now, search_term, str(len(res))))
        except:
            pass
    db_conn.close()
    return res
