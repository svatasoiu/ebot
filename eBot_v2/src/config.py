## Settings
BASEURL = "http://www.ebay.com/"
BASESEARCHURL = "http://www.ebay.com/sch/i.html?_from=R40%7CR40&_sacat=0&_nkw={}&_pgn={}&_skc={}&rt=nc"
MAX_ITEMS = 2500
MAX_THREADS = 20
ITEMS_PER_PAGE = 50
DEFAULT_SEARCH = "nexus 7"
LOGFILE = "/home/svatasoiu/git/EbayAnalyzer/logs/summary-%s.log"
# LOGFILE = "/home/svatasoi/ebot/logs/summary-%s.log"

## Item element Paths
ITEMPATH = "//div[@id='ResultSetItems']/ul/li"
ITEMTITLE = "h3[@class='lvtitle']"
PRICEPATH = "ul[@class='lvprices left space-zero']/li/span"
SELLERDETAILSPATH = "ul[@class='lvdetails left space-zero full-width']/li"
TIMELEFT = "ul[@class='lvdetails left space-zero full-width']/li/span[@class='tme']"
NUMBIDS = "ul[@class='lvprices left space-zero']/li[@class='lvformat bids']"
NUMRESULTSPATH = ".//*[@id='cbelm']/div[3]/h1/span[1]//text()"
