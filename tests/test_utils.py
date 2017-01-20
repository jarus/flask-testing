try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
from unittest import TestResult
from flask_testing import TestCase, LiveServerTestCase
from flask_testing.utils import ContextVariableDoesNotExist
from .flask_app import create_app


class TestSetup(TestCase):

    def create_app(self):
        return create_app()

    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)


class TestSetupFailure(TestCase):

    def _pre_setup(self):
        pass

    def test_setup_failure(self):
        '''Should not fail in _post_teardown if _pre_setup fails'''
        assert True

class TestTeardownGraceful(TestCase):

    def create_app(self):
        return create_app()

    def test_remove_testcase_attributes(self):
        """
        There should no exception after this test because teardown
        is graceful.
        """

        del self.app
        del self._ctx

class TestClientUtils(TestCase):

    def create_app(self):
        return create_app()

    def test_get_json(self):
        response = self.client.get("/ajax/")
        self.assertEqual(response.json, dict(name="test"))

    def test_status_failure_message(self):
        expected_message = 'my message'
        try:
            self.assertStatus(self.client.get('/'), 404, expected_message)
        except AssertionError as e:
            self.assertTrue(expected_message in str(e))

    def test_default_status_failure_message(self):
        expected_message = 'HTTP Status 404 expected but got 200'
        try:
            self.assertStatus(self.client.get('/'), 404)
        except AssertionError as e:
            self.assertTrue(expected_message in str(e))

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

    def test_assert_redirects_full_url(self):
        response = self.client.get("/external_redirect/")
        self.assertRedirects(response, "http://flask.pocoo.org/")

    def test_assert_redirects_failure_message(self):
        response = self.client.get("/")
        try:
            self.assertRedirects(response, "/anything")
        except AssertionError as e:
            self.assertTrue("HTTP Status 301, 302, 303, 305, 307 expected but got 200" in str(e))

    def test_assert_redirects_custom_message(self):
        response = self.client.get("/")
        try:
            self.assertRedirects(response, "/anything", "Custom message")
        except AssertionError as e:
            self.assertTrue("Custom message" in str(e))

    def test_assert_redirects_valid_status_codes(self):
        valid_redirect_status_codes = (301, 302, 303, 305, 307)

        for status_code in valid_redirect_status_codes:
            response = self.client.get("/redirect/?code=" + str(status_code))
            self.assertRedirects(response, "/")
            self.assertStatus(response, status_code)

    def test_assert_redirects_invalid_status_code(self):
        status_code = 200
        response = self.client.get("/redirect/?code=" + str(status_code))
        self.assertStatus(response, status_code)
        try:
            self.assertRedirects(response, "/")
        except AssertionError as e:
            self.assertTrue("HTTP Status 301, 302, 303, 305, 307 expected but got 200" in str(e))

    def test_assert_template_used(self):
        try:
            self.client.get("/template/")
            self.assert_template_used("index.html")
        except RuntimeError:
            pass

    def test_assert_template_not_used(self):
        self.client.get("/template/")
        try:
            self.assertRaises(AssertionError, self.assert_template_used, "invalid.html")
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

    def test_assert_context_custom_message(self):
        self.client.get("/template/")
        try:
            self.assert_context("name", "nothing", "Custom message")
        except AssertionError as e:
            self.assertTrue("Custom message" in str(e))
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

    def test_assert_bad_context_custom_message(self):
        self.client.get("/template/")
        try:
            self.assert_context("foo", "foo", "Custom message")
        except AssertionError as e:
            self.assertTrue("Custom message" in str(e))
        except RuntimeError:
            pass

    def test_assert_get_context_variable_not_exists(self):
        try:
            self.client.get("/template/")
            self.assertRaises(ContextVariableDoesNotExist,
                              self.get_context_variable, "foo")
        except RuntimeError:
            pass

    def test_assert_flashed_messages_succeed(self):
        try:
            self.client.get("/flash/")
            self.assertMessageFlashed("Flashed message")
        except RuntimeError:
            pass

    def test_assert_flashed_messages_failed(self):
        try:
            self.client.get("/flash/")
            self.assertRaises(AssertionError, self.assertMessageFlashed, "Flask-testing has assertMessageFlashed now")
        except RuntimeError:
            pass

    def test_assert_no_flashed_messages_fail(self):
        try:
            self.client.get("/no_flash/")
            self.assertRaises(AssertionError, self.assertMessageFlashed, "Flashed message")
        except RuntimeError:
            pass


class BaseTestLiveServer(LiveServerTestCase):

    def test_server_process_is_spawned(self):
        process = self._process

        # Check the process is spawned
        self.assertNotEqual(process, None)

        # Check the process is alive
        self.assertTrue(process.is_alive())

    def test_server_listening(self):
        response = urlopen(self.get_server_url())
        self.assertTrue(b'OK' in response.read())
        self.assertEqual(response.code, 200)


class TestLiveServer(BaseTestLiveServer):

    def create_app(self):
        app = create_app()
        app.config['LIVESERVER_PORT'] = 8943
        return app


class TestLiveServerOSPicksPort(BaseTestLiveServer):

    def create_app(self):
        app = create_app()
        app.config['LIVESERVER_PORT'] = 0
        return app


class TestNotRenderTemplates(TestCase):

    render_templates = False

    def create_app(self):
        return create_app()

    def test_assert_not_process_the_template(self):
        response = self.client.get("/template/")

        assert len(response.data) == 0

    def test_assert_template_rendered_signal_sent(self):
        self.client.get("/template/")

        self.assert_template_used('index.html')


class TestRenderTemplates(TestCase):

    render_templates = True

    def create_app(self):
        return create_app()

    def test_assert_not_process_the_template(self):
        response = self.client.get("/template/")

        assert len(response.data) > 0


class TestRestoreTheRealRender(TestCase):

    def create_app(self):
        return create_app()

    def test_assert_the_real_render_template_is_restored(self):
        test = TestNotRenderTemplates('test_assert_not_process_the_template')
        test_result = TestResult()
        test(test_result)

        assert test_result.wasSuccessful()

        response = self.client.get("/template/")

        assert len(response.data) > 0
