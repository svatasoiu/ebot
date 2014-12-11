import item
import analyzer
import db_config as db_constants
import mysql.connector

db_conn = mysql.connector.connect(**db_constants.DBCONFIG)
cursor = db_conn.cursor()

# search_terms_query = "SELECT SearchTerm FROM %s GROUP BY SearchTerm;" # could get search terms dynamically
search_terms = ["nexus 7", "iphone 6", "fifa 15 xbox one", "nike mercurial vapor superfly"]
items = {}
for term in search_terms:
    items[term] = []

# find all tables
table_names = ["ItemsWeek" + str(i) for i in range(3)]
generic_query = "SELECT EbayID, BidPrice, BINPrice, TimeLeft FROM `%s` WHERE SearchTerm='%s'"

def Decimal_to_float(dec):
    return float(dec) if dec is not None else None

# execute queries and
for search_term in search_terms:
    for table in table_names:
        query = generic_query % (table, search_term)
        print(query)
        try:
            cursor.execute(query)
        except:
            break
#         cursor.execute(query, (table, search_term))
        for (EbayID, BidPrice, BINPrice, TimeLeft) in cursor:
            items[search_term].append(item.Item(EbayID, "", "", Decimal_to_float(BINPrice), Decimal_to_float(BidPrice), TimeLeft, 0, search_term))
            
for search_term in search_terms:
    these_items = items[search_term]
    if len(these_items) > 0:
        print("Plotting price histograms for SearchTerm=%s" % search_term)
        analyzer.plotPriceHistograms(these_items)
        
        print("Plotting price vs timeLeft graphs for Search Term=%s" % search_term)
        analyzer.plotPriceVsTimeLeftGraphs(these_items)

cursor.close()
db_conn.close()