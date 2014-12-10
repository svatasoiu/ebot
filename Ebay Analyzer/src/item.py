'''
Created on Aug 5, 2014

@author: svatasoiu
'''
import selenium.common.exceptions, re
import config as constants
from datetime import datetime, date

def getElementTextWithDefault(elt, path, default = ""):
    try:
        return elt.find_element_by_xpath(path).text
    except selenium.common.exceptions.NoSuchElementException:
        return default

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
                add_item  = "INSERT INTO ItemsWeek" + str(1+(date.today() - date(2014, 11, 1)).days/7) + \
                    " (EbayID,Title,SellerName,BidPrice,BINPrice,TimeLeft,NumBids,SearchTerm) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    #                         " ON DUPLICATE KEY UPDATE EbayID=EbayID,Title=Title,SellerName=SellerName,BidPrice=BidPrice," \
    #                         "BINPrice=BINPrice,TimeLeft=TimeLeft,NumBids=NumBids,SearchTerm=SearchTerm;"
                item_data = (self.ebayID, self.title, self.seller_name, self.AUCprice, self.BINprice, self.time_left, self.num_bids, search_term)
                cursor.execute(add_item, item_data)
                db_conn.commit()
                cursor.close()
            except:
                time_now = datetime.now().strftime("%I:%M:%S%p")
                print("Error uploading item w/ ID = %s to MySQL" % self.ebayID)
                if logfile:
                    try:
                        logfile.write("%s: (term=%s) Error uploading item w/ ID = %s to MySQL\n" % (time_now, search_term, self.ebayID))
                    except:
                        pass
            finally:
                cursor.close()

    @classmethod
    def init_from_html(elt, db_conn, search_term="", logfile=None):
        ebayID = elt.get_attribute("id").replace("item","")
        title = elt.find_element_by_xpath(constants.ITEMTITLE).text
        seller_name = ""
        details = elt.find_elements_by_xpath(constants.SELLERDETAILSPATH)
        for d in details:
            t = d.text
            if "Seller" in t:
                m = re.search('^[^\(]+', t)
                x = m.group(0)
                seller_name = x.replace("Seller: ","")
                break
         
        print("%s (%s): %s" % (ebayID, seller_name, title))
        priceItems = elt.find_elements_by_xpath(constants.PRICEPATH)
        i = 0
        BINprice = None
        AUCprice = None
        for p in priceItems:
            try:
                if "bids" in p.text:
                    AUCprice = float(priceItems[i - 1].text[1:].split("\n")[0].replace(',',''))
                if "Now" in p.text:
                    BINprice = float(priceItems[i - 1].text[1:].split("\n")[0].replace(',',''))
                    # should be last
                    break
            except:
                print("Could not parse price for " + title)
                break
            i += 1
         
        try:
            txt = elt.find_element_by_xpath(constants.TIMELEFT).text
            print(txt)
            time_left = parse_time(txt)
        except:
            time_left = None
         
        try:
            txt = elt.find_element_by_xpath(constants.NUMBIDS).text
            print(txt)
            num_bids = int(txt.split("bid")[0].strip())
        except:
            num_bids = None
            
        return Item(ebayID, title, seller_name, BINprice, AUCprice, 
                 time_left, num_bids, search_term, db_conn, logfile)
        
#     def __init__(self, elt, db_conn, search_term="", logfile=None):
#         '''
#         Constructor
#         '''
#         self.ebayID = elt.get_attribute("id").replace("item","")
#         self.title = elt.find_element_by_xpath(constants.ITEMTITLE).text
#         self.seller_name = ""
#         details = elt.find_elements_by_xpath(constants.SELLERDETAILSPATH)
#         for d in details:
#             t = d.text
#             if "Seller" in t:
#                 m = re.search('^[^\(]+', t)
#                 x = m.group(0)
#                 self.seller_name = x.replace("Seller: ","")
#                 break
#         
#         print("%s (%s): %s" % (self.ebayID, self.seller_name, self.title))
#         priceItems = elt.find_elements_by_xpath(constants.PRICEPATH)
#         i = 0
#         self.BINprice = None
#         self.AUCprice = None
#         for p in priceItems:
#             try:
#                 if "bids" in p.text:
#                     self.AUCprice = float(priceItems[i - 1].text[1:].split("\n")[0].replace(',',''))
#                 if "Now" in p.text:
#                     self.BINprice = float(priceItems[i - 1].text[1:].split("\n")[0].replace(',',''))
#                     # should be last
#                     break
#             except:
#                 print("Could not parse price for " + self.title)
#                 break
#             i += 1
#         
#         try:
#             txt = elt.find_element_by_xpath(constants.TIMELEFT).text
#             print(txt)
#             self.time_left = parse_time(txt)
#         except:
#             self.time_left = None
#         
#         try:
#             txt = elt.find_element_by_xpath(constants.NUMBIDS).text
#             print(txt)
#             self.num_bids = int(txt.split("bid")[0].strip())
#         except:
#             self.num_bids = None
#         
#         # add to mysql db
#         cursor = db_conn.cursor()
#         try:
#             add_item  = "INSERT INTO ItemsWeek" + str(1+(date.today() - date(2014, 11, 1)).days/7) + \
#                 " (EbayID,Title,SellerName,BidPrice,BINPrice,TimeLeft,NumBids,SearchTerm) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
# #                         " ON DUPLICATE KEY UPDATE EbayID=EbayID,Title=Title,SellerName=SellerName,BidPrice=BidPrice," \
# #                         "BINPrice=BINPrice,TimeLeft=TimeLeft,NumBids=NumBids,SearchTerm=SearchTerm;"
#             item_data = (self.ebayID, self.title, self.seller_name, self.AUCprice, self.BINprice, self.time_left, self.num_bids, search_term)
#             cursor.execute(add_item, item_data)
#             db_conn.commit()
#             cursor.close()
#         except:
#             time_now = datetime.now().strftime("%I:%M:%S%p")
#             print("Error uploading item w/ ID = %s to MySQL" % self.ebayID)
#             if logfile:
#                 try:
#                     logfile.write("%s: (term=%s) Error uploading item w/ ID = %s to MySQL\n" % (time_now, search_term, self.ebayID))
#                 except:
#                     pass
#         finally:
#             cursor.close()
    
    def toString(self):
        return self.title + ": " + str(self.BINprice) + "/" + str(self.AUCprice)

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