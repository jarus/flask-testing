import unittest

from flask_testing import is_twill_available

from .test_twill import TestTwill, TestTwillDeprecated
from .test_utils import TestSetup, TestSetupFailure, TestClientUtils, \
        TestLiveServer, TestTeardownGraceful, TestRenderTemplates, \
        TestNotRenderTemplates, TestRestoreTheRealRender, \
        TestLiveServerOSPicksPort


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    suite.addTest(unittest.makeSuite(TestSetupFailure))
    suite.addTest(unittest.makeSuite(TestClientUtils))
    suite.addTest(unittest.makeSuite(TestLiveServer))
    suite.addTest(unittest.makeSuite(TestLiveServerOSPicksPort))
    suite.addTest(unittest.makeSuite(TestTeardownGraceful))
    suite.addTest(unittest.makeSuite(TestRenderTemplates))
    suite.addTest(unittest.makeSuite(TestNotRenderTemplates))
    suite.addTest(unittest.makeSuite(TestRestoreTheRealRender))
    if is_twill_available:
        suite.addTest(unittest.makeSuite(TestTwill))
        suite.addTest(unittest.makeSuite(TestTwillDeprecated))
    else:
        print("!!! Skipping tests of Twill components\n")
    return suite
