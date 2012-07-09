import unittest

from test_utils import TestSetup, TestClientUtils
from test_twill import TestTwill, TestTwillDeprecated

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    suite.addTest(unittest.makeSuite(TestClientUtils))
    suite.addTest(unittest.makeSuite(TestTwill))
    suite.addTest(unittest.makeSuite(TestTwillDeprecated))
    return suite

