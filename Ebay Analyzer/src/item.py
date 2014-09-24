'''
Created on Aug 5, 2014

@author: svatasoiu
'''
import selenium.common.exceptions, re
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

    def __init__(self, elt, db_conn):
        '''
        Constructor
        '''
        self.ebayID = elt.get_attribute("id").replace("item","")
        self.title = elt.find_element_by_xpath(constants.ITEMTITLE).text
        self.seller_name = ""
        details = elt.find_elements_by_xpath(constants.SELLERDETAILSPATH)
        for d in details:
            t = d.text
            if "Seller" in t:
                m = re.search('^[^\(]+', t)
                x = m.group(0)
                self.seller_name = x.replace("Seller: ","")
                break
        
        print("%s (%s): %s" % (self.ebayID, self.seller_name, self.title))
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
            
        # add to mysql db
        cursor = db_conn.cursor()
        add_item  = "INSERT INTO Items (EbayID,Title,SellerName,BidPrice,BINPrice) VALUES (%s,%s,%s,%s,%s)" \
                    " ON DUPLICATE KEY UPDATE EbayID=EbayID,Title=Title,SellerName=SellerName,BidPrice=BidPrice,BINPrice=BINPrice;"
        item_data = (self.ebayID, self.title, self.seller_name, self.AUCprice, self.BINprice)
        cursor.execute(add_item, item_data)
        db_conn.commit()
        cursor.close()
        
    
    def toString(self):
        return self.title + ": " + str(self.BINprice) + "/" + str(self.AUCprice)