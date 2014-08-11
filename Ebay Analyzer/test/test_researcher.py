'''
Created on Aug 10, 2014

@author: svatasoiu
'''
import unittest, browser, researcher

class Test(unittest.TestCase):

    def testGetItems(self):
        w = browser.openBrowser()
        browser.openToPage(w)
        browser.getRelated(w, "nexus 7")
        researcher.setupCustomSearch(w)
        items = researcher.retrieveAllSimilarItems(w)
        self.assertGreater(len(items), 0, "Possibly need to update paths, not enough items found")
        w.close()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()