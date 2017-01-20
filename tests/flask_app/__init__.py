from flask import (
    Flask,
    Response,
    abort,
    redirect,
    jsonify,
    render_template,
    url_for,
    flash,
    request
)


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super secret testing key'

    @app.route("/")
    def index():
        return Response("OK")

    @app.route("/template/")
    def index_with_template():
        return render_template("index.html", name="test")

    @app.route("/flash/")
    def index_with_flash():
        flash("Flashed message")
        return render_template("index.html")

    @app.route("/no_flash/")
    def index_without_flash():
        return render_template("index.html")

    @app.route("/oops/")
    def bad_url():
        abort(404)

    @app.route("/redirect/")
    def redirect_to_index():
        code = request.args.get('code') or 301
        return redirect(url_for("index"), code=code)

    @app.route("/external_redirect/")
    def redirect_to_flask_docs():
        return redirect("http://flask.pocoo.org/")

    @app.route("/ajax/")
    def ajax():
        return jsonify(name="test")

    @app.route("/forbidden/")
    def forbidden():
        abort(403)

    @app.route("/unauthorized/")
    def unauthorized():
        abort(401)

    @app.route("/internal_server_error/")
    def internal_server_error():
        abort(500)

    return app
