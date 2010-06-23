from flask import Flask, Response, abort, redirect, url_for

from flaskext.testing import TestCase

def create_app():

    app = Flask(__name__)
    
    @app.route("/")
    def index():
        return Response("OK")

    @app.route("/oops/")
    def bad_url():
        abort(404)

    @app.route("/redirect/")
    def redirect_to_index():
        return redirect(url_for("index"))

    return app

class TestSetup(TestCase):

    def create_app(self):
        return create_app()

    def test_setup(self):

        assert self.app
        assert self.client
        assert self._ctx


class TestClientUtils(TestCase):

    def create_app(self):
        return create_app()

    def test_assert_200(self):

        response = self.client.get("/")
        self.assert200(response)

    def test_assert_404(self):

        response = self.client.get("/oops/")
        self.assert404(response)

    def test_assert_redirects(self):

        response = self.client.get("/redirect/")
        self.assertRedirects(response, "/")
