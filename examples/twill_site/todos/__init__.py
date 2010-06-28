from flask import Flask, render_template, flash, redirect, url_for

TWILL_ENABLED = True
SECRET_KEY = 'secret'
DEBUG = True

def create_app():

    app = Flask(__name__)
    app.config.from_object(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/submit/", methods=("POST",))
    def submit():
        flash("Form submitted")
        return redirect(url_for("index"))
    return app
