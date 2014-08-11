'''
Created on Aug 5, 2014

@author: svatasoiu
'''
import selenium.common.exceptions
import config as constants

def getElementTextWithDefault(elt, path, default = ""):
    try:
        return elt.find_element_by_xpath(path).text
    except selenium.common.exceptions.NoSuchElementException:
        return default

class Item:
    '''
    An Item has a title, and optional BIN and AUC prices
    '''

    def __init__(self, elt):
        '''
        Constructor
        '''
        self.title = elt.find_element_by_xpath(constants.ITEMTITLE).text
        
        priceItems = elt.find_elements_by_xpath(constants.PRICEPATH)
        i = 0
        self.BINprice = None
        self.AUCprice = None
        for p in priceItems:
            try:
                if "bids" in p.text:
                    self.AUCprice = float(priceItems[i - 1].text[1:].split("\n")[0].replace(',',''))
                if "Now" in p.text:
                    self.BINprice = float(priceItems[i - 1].text[1:].split("\n")[0].replace(',',''))
                    # should be last
                    break
            except:
                print("Could not parse price for " + self.title)
                break
            i += 1
    
    def toString(self):
        return self.title + ": " + str(self.BINprice) + "/" + str(self.AUCprice)