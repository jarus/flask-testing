from flaskext.testing import TwillTestCase

from todos import create_app

class TestViews(TwillTestCase):

    def create_app(self):
        return create_app()

    def test_manually(self):

        self.browser.go(self.make_twill_url("/"))
        self.browser.showforms()
        self.browser.submit(0)

    def test_bad_manually(self):
        """
        This will fail !
        """
        self.browser.go(self.make_twill_url("/foo/"))
        self.browser.showforms()
        self.browser.submit(1)

