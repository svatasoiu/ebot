'''
Created on Aug 10, 2014

@author: svatasoiu
'''
from statistics import mean, stdev
import pylab as P

def getExistingPrices(items):
    """ Gets all non-None prices from items"""
    return [item.BINprice for item in items if item.BINprice is not None]

def filterOutliers(prices):
    """ Removes outliers from the prices list. """
    return prices
    #mu = mean(prices)
    #sigma = stdev(prices)
    #return list(filter(lambda p: p > mu - 0.8*sigma, prices))

def plotPriceHistogram(items):
    """ Plots a histogram of the price data of items """
    prices = filterOutliers(getExistingPrices(items))
    
    n, bins, patches = P.hist(prices, 10, normed=1, histtype='stepfilled')
    P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
    P.show()
