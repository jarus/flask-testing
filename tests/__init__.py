import unittest

from test_base import TestSetup, TestTwill, TestClientUtils, \
TestTwillDeprecated

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    suite.addTest(unittest.makeSuite(TestTwill))
    suite.addTest(unittest.makeSuite(TestClientUtils))
    suite.addTest(unittest.makeSuite(TestTwillDeprecated))
    return suite

