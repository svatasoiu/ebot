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
    classdocs
    '''

    def __init__(self, elt):
        '''
        Constructor
        '''
        self.elt = elt
        self.title = elt.find_element_by_xpath(constants.ITEMTITLE).text
        
        priceItems = elt.find_elements_by_xpath(constants.PRICEPATH)
        # need to parse priceItems (3 cases: 1) only BIN, 2) only auction, 3) both prices)
        try:
            self.BINprice = float(getElementTextWithDefault(self.elt, constants.ITEMBINPRICE)[1:])
        except:
            print("Item " + self.title + " does not have a BIN price")
            self.BINprice = None
        try:
            self.AUCprice = float(getElementTextWithDefault(self.elt, constants.ITEMAUCPRICE)[1:])
        except:
            print("Item " + self.title + " does not have an auction price")
            self.AUCprice = None
        
    
    def toString(self):
        return self.title + ": " + str(self.BINprice) + "/" + str(self.AUCprice)