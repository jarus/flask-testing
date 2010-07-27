"""
Flask-Testing
--------------

Flask unittest integration.

Links
`````

* `documentation <http://packages.python.org/Flask-Testing>`_
* `development version
  <http://bitbucket.org/danjac/flask-testing/get/tip.gz#egg=Flask-Testing-dev>`_

"""
from setuptools import setup

setup(
    name='Flask-Testing',
    version='0.2.2',
    url='http://bitbucket.org/danjac/flask-testing',
    license='BSD',
    author='Dan Jacob',
    author_email='danjac354@gmail.com',
    description='Unit testing for Flask',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    test_suite="nose.collector",
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'twill',
        'simplejson',
    ],
    tests_require=[
        'nose',
        'blinker',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
