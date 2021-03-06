# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import os
import sys

from setuptools import setup, find_packages

# here = os.path.abspath(os.path.dirname(__file__))
# README = open(os.path.join(here, '../README.rst')).read()
# CHANGES = open(os.path.join(here, '../CHANGES.txt')).read()
# long_desc = README + '\n\n' + CHANGES

requires = [
	'setuptools',
	'pyramid>=1.3',
	'SQLAlchemy',
	'transaction',
#	'pyramid_chameleon',
	'pyramid_jinja2',
	'pyramid_tm',
	'pyramid_debugtoolbar',
	'pyramid_exclog',
	'pyramid_services',
	'zope.sqlalchemy',
#	'pyramid_simpleform',
	'cryptacular',
	'waitress',
	'pycrypto',
	'webtest',
	'rdflib',
	'cornice',
	'colander',
]

if sys.version_info[:3] < (2,5,0):
    raise RuntimeError('This application requires Python 2.6+')

setup(name='birda',
      version='0.1.1',
      description='Builder of Interfaces for RDF Data Authoring (BIRD-A)',
      long_description="",
      classifiers=[
        "Framework :: Pylons",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author="Francesco Caliumi, Silvio Peroni",
      author_email="francesco.caliumi@gmail.com, silvio.peroni@unibo.it",
      url='...',
      license="...",
      keywords='birda rdf ontology',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='birda.tests',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = birda:main
      [console_scripts]
      birda_init_db = birda.scripts.initialize_db:main
      """,
      paster_plugins=['pyramid']
)
