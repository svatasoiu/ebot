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
        self.BINprice = getElementTextWithDefault(self.elt, constants.ITEMBINPRICE)
        self.AUCprice = getElementTextWithDefault(self.elt, constants.ITEMAUCPRICE)
    
    def toString(self):
        return self.title + ": " + self.BINprice + "/" + self.AUCprice