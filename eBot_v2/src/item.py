'''
Created on Aug 5, 2014

@author: svatasoiu
'''
import re
import config as constants
from datetime import datetime

def xpathWithDefault(xml, path, default=""):
    res = xml.xpath(path)
    return default if len(res) == 0 else res[0]

class Item:
    '''
    An Item has a title, and optional BIN and AUC prices
    '''

    def __init__(self, ebayID, title, seller_name, BINprice, AUCprice, 
                 time_left, num_bids, search_term, db_conn=None, logfile=None):
        self.ebayID = ebayID
        self.title = title
        self.seller_name = seller_name
        self.BINprice = BINprice
        self.AUCprice = AUCprice
        self.time_left = time_left
        self.num_bids = num_bids
        
        # add to mysql db
        if db_conn:
            cursor = db_conn.cursor()
            try:
                add_item  = "INSERT INTO Items" + \
                    " (EbayID,Title,SellerName,BidPrice,BINPrice,TimeLeft,NumBids,SearchTerm) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                item_data = (str(self.ebayID), str(self.title), str(self.seller_name), str(self.AUCprice) if self.AUCprice else None, 
                             str(self.BINprice) if self.BINprice else None, str(self.time_left), str(self.num_bids), str(search_term))
                cursor.execute(add_item, item_data)
                db_conn.commit()
            except Exception as e:
                print e
                time_now = datetime.now().strftime("%I:%M:%S%p")
                print("Error uploading item w/ ID = %s to MySQL" % self.ebayID)
                if logfile:
                    try:
                        logfile.write("%s: (term=%s) Error uploading item w/ ID = %s to MySQL\n" % (time_now, search_term, self.ebayID))
                    except:
                        pass
            finally:
                cursor.close()
        
    def toString(self):
        return self.title + ": " + str(self.BINprice) + "/" + str(self.AUCprice)

def lxml_xpath(s):
    return './' + s + '//text()'

def init_from_html_lxml(xml, db_conn, search_term="", logfile=None):
    ebayID = xml.attrib["id"].replace("item", "")
#     print ebayID
    title = xpathWithDefault(xml, lxml_xpath(constants.ITEMTITLE))
#     print title
    seller_name = ""
#     print lxml_xpath(constants.SELLERDETAILSPATH)
    details = xml.xpath('./'+constants.SELLERDETAILSPATH)
    for t in details:
        if "Seller" in t:
            m = re.search('^[^\(]+', t)
            x = m.group(0)
            seller_name = x.replace("Seller: ", "")
            break
        
#     print("%s (%s): %s" % (ebayID, seller_name, title))
    priceItems = xml.xpath(lxml_xpath(constants.PRICEPATH))
    i = 0
    BINprice = None
    AUCprice = None
    for p in priceItems:
        try:
            if "bids" in p:
                AUCprice = float(priceItems[i - 1].lstrip()[1:].split("\n")[0].replace(',', ''))
            if "Now" in p:
                BINprice = float(priceItems[i - 1].lstrip()[1:].split("\n")[0].replace(',', ''))
        except:
            pass
#             print("Could not parse price for " + title)
        i += 1
    
    try:
        txt = xpathWithDefault(xml, lxml_xpath(constants.TIMELEFT))
        time_left = parse_time(txt)
    except:
        time_left = None
    
    try:
        txt = xpathWithDefault(xml, lxml_xpath(constants.NUMBIDS))
        num_bids = int(txt.split("bid")[0].strip())
    except:
        num_bids = None
            
    return Item(ebayID, title, seller_name, BINprice, AUCprice,
                 time_left, num_bids, search_term, db_conn, logfile)

"turns time_string into an integer number of seconds"
def parse_time(time_string):
    formatted_time = time_string.split("left")[0].strip()
    seconds = re.match("(\d+)s", formatted_time)
    minutes = re.match("(\d+)m", formatted_time)
    hours = re.match("(\d+)h", formatted_time)
    days = re.match("(\d+)d", formatted_time)
    
    seconds_left = 0
    seconds_left += int(seconds.group(1)) if seconds else 0
    seconds_left += 60*int(minutes.group(1)) if minutes else 0
    seconds_left += 3600*int(hours.group(1)) if hours else 0
    seconds_left += 24*3600*int(days.group(1)) if days else 0
    return seconds_left # seconds
