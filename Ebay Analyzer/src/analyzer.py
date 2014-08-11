'''
Created on Aug 10, 2014

@author: svatasoiu
'''
from statistics import mean, stdev
import pylab as P
from time import time

def getExistingBINPrices(items):
    """ Gets all non-None BIN prices from items"""
    return [item.BINprice for item in items if item.BINprice is not None]

def getExistingAUCPrices(items):
    """ Gets all non-None auction prices from items"""
    return [item.AUCprice for item in items if item.AUCprice is not None]

def filterOutliers(prices):
    """ Removes outliers from the prices list. """
    return prices
    #mu = mean(prices)
    #sigma = stdev(prices)
    #return list(filter(lambda p: p > mu - 0.8*sigma, prices))

def plotPriceHistogram(items, f):
    """ Plots a histogram of the price data of items """
    start = time()
    prices = filterOutliers(f(items))
    
    print("Plotting Histogram")
    (_, _, patches) = P.hist(prices, 10, histtype='stepfilled')
    P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
    P.xlabel("Price ($)")
    P.ylabel("Number of Items in Bucket")
    
    (avg, count, sigma) = (mean(prices), len(prices), stdev(prices))
    print("{:d} items at an average price of ${:.2f} w/ a standard deviation of ${:.2f}".format(count, avg, sigma))
    
    print("Analysis took {:.2f}s".format(time() - start))
    P.show()

def plotPriceHistograms(items):
    P.title("Buy It Now Prices")
    plotPriceHistogram(items, getExistingBINPrices)
    P.title("Auction Prices")
    plotPriceHistogram(items, getExistingAUCPrices)
