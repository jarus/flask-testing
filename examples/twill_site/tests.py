from flaskext.testing import TestCase, Twill

from todos import create_app

class TestViews(TestCase, Twill):

    def create_app(self):
        app = create_app()
        self.twill = Twill(app)
        return app

    def test_manually(self):

        self.twill.browser.go(self.twill.url("/"))
        self.twill.browser.showforms()
        self.twill.browser.submit(0)

    def test_bad_manually(self):
        """
        This will fail !
        """
        self.twill.browser.go(self.twill.url("/foo/"))
        self.twill.browser.showforms()
        self.twill.browser.submit(1)


