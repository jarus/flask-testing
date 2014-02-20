import unittest

from flask_testing import is_twill_available

from .test_utils import TestSetup, TestClientUtils, TestLiveServer
from .test_twill import TestTwill, TestTwillDeprecated


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    suite.addTest(unittest.makeSuite(TestClientUtils))
    suite.addTest(unittest.makeSuite(TestLiveServer))
    if is_twill_available:
        suite.addTest(unittest.makeSuite(TestTwill))
        suite.addTest(unittest.makeSuite(TestTwillDeprecated))
    else:
        print("!!! Skipping tests of Twill components\n")
    return suite
