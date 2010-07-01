from flaskext.testing import TwillTestCase

from twill import commands as tc

from todos import create_app

class TestViews(TwillTestCase):

    def create_app(self):
        return create_app()

    def test_string(self):
        
        s = """
go /
submit 0
        """
    
        self.execute_twill_string(s)

    def test_script(self):

        self.execute_twill_script("scripts/simple.twill")

    def test_manually(self):

        tc.go(self.twill_url("/"))
        tc.showforms()
        tc.submit(0)

    def test_bad_manually(self):
        """
        This will fail !
        """
        tc.go(self.twill_url("/foo/"))
        tc.showforms()
        tc.submit(1)

