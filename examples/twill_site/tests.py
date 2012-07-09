from twill.browser import TwillException
from flask_testing import TestCase, Twill

from todos import create_app

class TestViews(TestCase):

    def create_app(self):
        app = create_app()
        self.twill = Twill(app)
        return app

    def test_manually(self):
        with self.twill as t:
            t.browser.go(self.twill.url("/"))
            t.browser.showforms()
            t.browser.submit(0)

    def test_bad_manually(self):
        with self.twill as t:
            t.browser.go(self.twill.url("/foo/"))
            t.browser.showforms()
            self.assertRaises(TwillException, t.browser.submit, 1)
