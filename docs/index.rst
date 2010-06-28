flask-testing
======================================

.. module:: flask-testing

The **Flask-Testing** extension provides unit testing utilities for Flask.

Source code and issue tracking at `Bitbucket`_.

Installing Flask-Testing
------------------------

Install with **pip** and **easy_install**::

    pip install Flask-Testing

or download the latest version from Bitbucket::

    hg clone http://bitbucket.org/danjac/flask-testing

    cd flask-testing

    python setup.py develop

If you are using **virtualenv**, it is assumed that you are installing flask-testing
in the same virtualenv as your Flask application(s).

Writing unit tests
------------------

Simply subclass the ``TestCase`` class::

    from flaskext.testing import TestCase

    class MyTest(TestCase):

        pass


You must specify the ``create_app`` method, which should return a Flask instance::

    from flaskext.testing import TestCase

    class MyTest(TestCase):

        def create_app(self):

            app = Flask(__name__)
            app.config['TESTING'] = True
            return app

If you don't define ``create_app`` a ``NotImplementedError`` will be raised.

Using with Twill
----------------

`Twill <http://twill.idyll.org/>`_ is a simple language for browing the Web through
a command line interface. You can use it in conjunction with ``TestCase`` to write
functional tests for your views.

To use Twill with ``TestCase`` you need the following configuration settings:

    * ``TWILL_ENABLED`` : default ``False``
    * ``TWILL_SCHEME`` : default ``http://``
    * ``TWILL_HOST`` : default ``localhost``
    * ``TWILL_PORT`` : default ``5000``

If ``TWILL_ENABLED`` is set to ``True`` then Twill is initialized ready for use.

In addition a number of helper methods are provided for Twill : see the API documentation
for details.

API
---

.. module:: flaskext.testing

.. class:: TestCase
        
    Subclass of ``unittest.TestCase``. When run the following properties are defined:

        * ``self.app`` : Flask application defined by ``create_app``
        * ``self.client`` : Test client instance
    
    The Flask application test context is created and disposed of inside the test run.

    .. method:: create_app()
        
        Returns a Flask app instance. If not defined raises ``NotImplementedError``.
    
    .. method:: assertRedirects(response, location)
        
        Checks if HTTP response and redirect URL matches location.

        :param response: Response returned from test client
        :param location: URL (automatically prefixed by `http://localhost`)

    .. method:: assert200(response)
        
        Checks if ``response.status_code`` == 200

        :param response: Response returned from test client

    .. method:: assert404(response)
        
        Checks if ``response.status_code`` == 404

        :param response: Response returned from test client

    .. method:: getJSON(response)

        Returns Pythonized data from Response if JSON

        :param response: Response returned from test client

    .. method:: assertJSONEquals(response, name, value)

        If JSON returned in dict format, checks if ``name`` in dict and 
        that ``name`` equals ``value``.
        
        :param response: Response returned from test client
        :param name: name in dict
        :param value: value of dict[name]

    .. method:: twill_url(url)

        Creates full URL for Twill tests, based on ``TWILL_SCHEME``,
        ``TWILL_HOST`` and ``TWILL_PORT`` settings.

        :param url: relative URL, e.g. "/"

    .. method:: execute_twill_string(string, initial_url=None)

        Executes a Twill script inside a string.

        :param string: string containing Twill commands
        :param initial_url: initial_url for commands (uses "/" by default)

    .. method:: execute_twill_script(script, initial_url=None)

        Executes a Twill script in a file.

        :param script: filename of script
        :param initial_url: initial_url for commands (uses "/" by default)
        
.. _Flask: http://flask.pocoo.org
.. _Bitbucket: http://bitbucket.org/danjac/flask-testing
