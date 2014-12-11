'''
Created on Aug 10, 2014

@author: svatasoiu
'''
#from statistics import mean, stdev
import pylab as P
from time import time
from numpy import std, mean

def max_price(mu, sigma):
    return mu + 3*sigma

def getExistingBINPrices(items):
    """ Gets all non-None BIN prices from items"""
    return [item.BINprice for item in items if item.BINprice is not None]

def getExistingAUCPrices(items):
    """ Gets all non-None auction prices from items"""
    return [item.AUCprice for item in items if item.AUCprice is not None]

def filterOutliers(prices):
    """ Removes outliers from the prices list. """
    mu = mean(prices)
    sigma = std(prices)
    return list(filter(lambda p: p < max_price(mu, sigma), prices))

def plotPriceHistogram(items, extract_prices):
    """ Plots a histogram of the price data of items """
    start = time()
    prices = filterOutliers(extract_prices(items))
    
    print("Plotting Histogram")
    (_, _, patches) = P.hist(prices, 10, histtype='stepfilled')
    P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
    P.xlabel("Price ($)")
    P.ylabel("Number of Items in Bucket")
    
    #(avg, count, sigma) = (mean(prices), len(prices), stdev(prices))
    #print("{0:d} items at an average price of ${0:.2f} w/ a standard deviation of ${0:.2f}".format(count, avg, sigma))
    
    print("Analysis took {0:.2f}s".format(time() - start))
    P.show()

def plotPriceHistograms(items):
    P.title("Buy It Now Price Histogram")
    plotPriceHistogram(items, getExistingBINPrices)
    P.title("Auction Price Histogram")
    plotPriceHistogram(items, getExistingAUCPrices)
    
def plotPriceVsTimeLeft(items, price_name):
    time_left = []
    prices = []
    for item in items:
        t_l = item.time_left
        price = getattr(item, price_name)
        if t_l is not None and price is not None:
            time_left.append(t_l)
            prices.append(price)
    P.xlabel("Time Left In Auction (s)")
    P.ylabel("Price ($)")
    P.scatter(time_left, prices, alpha=0.5)
    P.show()

def plotPriceVsTimeLeftGraphs(items):
    P.title("Buy It Now Price vs TimeLeft")
    plotPriceVsTimeLeft(items, "BINprice")
    P.title("Auction Price vs TimeLeft")
    plotPriceVsTimeLeft(items, "AUCprice")
