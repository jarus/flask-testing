import urllib2
from flask_testing import TestCase, LiveServerTestCase
from flask_testing.utils import ContextVariableDoesNotExist
from flask_app import create_app

class TestSetup(TestCase):

    def create_app(self):
        return create_app()

    def test_setup(self):

        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)

class TestClientUtils(TestCase):

    def create_app(self):
        return create_app()
    
    def test_get_json(self):
        response = self.client.get("/ajax/")
        self.assertEqual(response.json, dict(name="test"))

    def test_assert_200(self):
        self.assert200(self.client.get("/"))

    def test_assert_404(self):
        self.assert404(self.client.get("/oops/"))

    def test_assert_403(self):
        self.assert403(self.client.get("/forbidden/"))
    
    def test_assert_401(self):
        self.assert401(self.client.get("/unauthorized/"))

    def test_assert_405(self):
        self.assert405(self.client.post("/"))

    def test_assert_redirects(self):
        response = self.client.get("/redirect/")
        self.assertRedirects(response, "/")

    def test_assert_template_used(self):
        try:
            response = self.client.get("/template/")
            self.assert_template_used("index.html")
        except RuntimeError:
            pass

    def test_assert_template_not_used(self):
        response = self.client.get("/")
        try:
            self.assert_template_used("index.html")
            assert False
        except AssertionError:
            pass
        except RuntimeError:
            pass

    def test_get_context_variable(self):
        try:
            response = self.client.get("/template/")
            self.assertEqual(self.get_context_variable("name"), "test")
        except RuntimeError:
            pass

    def test_assert_context(self):
        try:
            response = self.client.get("/template/")
            self.assert_context("name", "test")
        except RuntimeError:
            pass

    def test_assert_bad_context(self):
        try:
            response = self.client.get("/template/")
            self.assertRaises(AssertionError, self.assert_context,
                              "name", "foo")
            self.assertRaises(AssertionError, self.assert_context,
                              "foo", "foo")
        except RuntimeError:
            pass

    def test_assert_get_context_variable_not_exists(self):
        try:
            response = self.client.get("/template/")
            self.assertRaises(ContextVariableDoesNotExist, 
                              self.get_context_variable, "foo")
        except RuntimeError:
            pass

class TestLiveServer(LiveServerTestCase):

        def setUp(self):
            self.port = 8943
            super(TestLiveServer, self).setUp()

        def create_app(self):
            return create_app()

        def test_server_process_is_spawned(self):
            process = self._process

            # Check the process is spawned
            self.assertIsNotNone(process)
            
            # Check the process is alive 
            self.assertTrue(process.is_alive())

        def test_server_listening(self):
            response = urllib2.urlopen(self.get_server_url())
            self.assertIn('OK', response.read())
            self.assertEqual(response.code, 200)
