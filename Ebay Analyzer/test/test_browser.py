'''
Created on Aug 5, 2014

@author: svatasoiu
'''
import unittest, browser
import config as constants

class Test(unittest.TestCase):
    def setUp(self):
        self.w = browser.openBrowser(False)

    def tearDown(self):
        self.w.close()

    def testGetRelated(self):
        browser.openToPage(self.w)
        self.assertEqual(self.w.current_url, constants.BASEURL)
        rel = browser.getRelated(self.w, "nexus 7")
        self.assertTrue(len(rel) > 0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()