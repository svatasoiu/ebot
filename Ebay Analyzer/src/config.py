## Settings
BASEURL = "http://www.ebay.com/"
PHANTOMPATH = "/home/svatasoi/phantomjs-1.9.7-linux-i686/bin/phantomjs"
MAXPAGES = 2
DEFAULT_SEARCH = "nexus 7"
LOGFILE = "logs/summary-%s.log"

## Paths to search box and settings
SEARCHBOXPATH = "//div[@id='gh-ac-box2']/input"
SEARCHSUBMIT_ID = "gh-btn"
RELATEDPATH = "//div[@id='RelatedSearchesContainer']/span[@class='rls']/a"

## Pagination path
PAGINATIONPATH = "//table[@id='Pagination']/tbody/tr/td[@class='pagn-next']/a[@class='gspr next']"

## Item element Paths
ITEMPATH = "//div[@id='ResultSetItems']/ul/li"
ITEMTITLE = "h3[@class='lvtitle']"
PRICEPATH = "ul[@class='lvprices left space-zero']/li/span"
SELLERDETAILSPATH = "ul[@class='lvdetails left space-zero full-width']/li"
TIMELEFT = "ul[@class='lvdetails left space-zero full-width']/li/span[@class='tme']"
NUMBIDS = "ul[@class='lvprices left space-zero']/li[@class='lvformat bids']"
