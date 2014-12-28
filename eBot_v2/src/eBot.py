#! /usr/bin/python2.7

import researcher, analyzer
import config as constants
from time import time
from datetime import date
from optparse import OptionParser
import db_config as db_constants
# import mysql.connector
from db_pool import DBPool

# arguments 

parser = OptionParser()
parser.add_option("-s", "--search_term", dest="search_term", default=constants.DEFAULT_SEARCH, help="the term to search for")
parser.add_option("-g", action="store_true", dest="graph", default=False, help="to graph or not to graph")
parser.add_option("-w", action="store_true", dest="windowed", default=False, help="to window or not to window")
parser.add_option("-n", "--max_items", type=int, dest="max_items", default=constants.MAX_ITEMS, help="max number of items to scrape")
(options, args) = parser.parse_args()

# start searching
start = time()
ti = start
search_term = options.search_term

# get items
db_pool = DBPool(db_constants.DBCONFIG, pool_size=20)
# db_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="conn_pool", pool_size=constants.MAX_THREADS, **db_constants.DBCONFIG)

with open(constants.LOGFILE % date.today().strftime("%m-%d-%y"), 'a') as logfile:
    researcher = researcher.Researcher(constants.BASESEARCHURL, options.max_items, search_term, db_pool, logfile)
    queue = researcher.scrape_all_pages()
    queue.join()

tf = time()
print("Retrieval took {0:.2f}s".format(tf - ti))
ti = tf

# analyze and report on items
if options.graph:
    analyzer.plotPriceHistograms(researcher.all_items)
    analyzer.plotPriceVsTimeLeftGraphs(researcher.all_items)
end = time()

# close
print("Total time: {0:.2f}s".format(end - start))
