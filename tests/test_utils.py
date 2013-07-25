import urllib2
from unittest import TestResult
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

    def test_assert_500(self):
        self.assert500(self.client.get("/internal_server_error/"))

    def test_assert_redirects(self):
        response = self.client.get("/redirect/")
        self.assertRedirects(response, "/")

    def test_assert_template_used(self):
        try:
            self.client.get("/template/")
            self.assert_template_used("index.html")
        except RuntimeError:
            pass

    def test_assert_template_not_used(self):
        self.client.get("/")
        try:
            self.assert_template_used("index.html")
            assert False
        except AssertionError:
            pass
        except RuntimeError:
            pass

    def test_get_context_variable(self):
        try:
            self.client.get("/template/")
            self.assertEqual(self.get_context_variable("name"), "test")
        except RuntimeError:
            pass

    def test_assert_context(self):
        try:
            self.client.get("/template/")
            self.assert_context("name", "test")
        except RuntimeError:
            pass

    def test_assert_bad_context(self):
        try:
            self.client.get("/template/")
            self.assertRaises(AssertionError, self.assert_context,
                              "name", "foo")
            self.assertRaises(AssertionError, self.assert_context,
                              "foo", "foo")
        except RuntimeError:
            pass

    def test_assert_get_context_variable_not_exists(self):
        try:
            self.client.get("/template/")
            self.assertRaises(ContextVariableDoesNotExist,
                              self.get_context_variable, "foo")
        except RuntimeError:
            pass


class TestLiveServer(LiveServerTestCase):

        def create_app(self):
            app = create_app()
            app.config['LIVESERVER_PORT'] = 8943
            return app

        def test_server_process_is_spawned(self):
            process = self._process

            # Check the process is spawned
            self.assertNotEqual(process, None)

            # Check the process is alive
            self.assertTrue(process.is_alive())

        def test_server_listening(self):
            response = urllib2.urlopen(self.get_server_url())
            self.assertTrue('OK' in response.read())
            self.assertEqual(response.code, 200)


class TestNotRenderTemplates(TestCase):

    render_templates = False

    def create_app(self):
        return create_app()

    def test_assert_not_process_the_template(self):
        response = self.client.get("/template/")

        assert "" == response.data

    def test_assert_template_rendered_signal_sent(self):
        self.client.get("/template/")

        self.assert_template_used('index.html')


class TestRenderTemplates(TestCase):

    render_templates = True

    def create_app(self):
        return create_app()

    def test_assert_not_process_the_template(self):
        response = self.client.get("/template/")

        assert "" != response.data


class TestRestoreTheRealRender(TestCase):

    def create_app(self):
        return create_app()

    def test_assert_the_real_render_template_is_restored(self):
        test = TestNotRenderTemplates('test_assert_not_process_the_template')
        test_result = TestResult()
        test(test_result)

        assert test_result.wasSuccessful()

        response = self.client.get("/template/")

        assert "" != response.data
