#!/usr/bin/env python

from distutils.core import setup

setup(name='PyFeed',
      version='0.7.4',
      description='Modules for working with syndication feeds',
#      long_description="""long description here""",
      license='BSD',
      author='Steve R. Hastings',
      author_email='steve@hastings.org',
      url='http://www.blarg.net/~steveha/pyfeed.html',
      packages=['feed', 'feed.date'],
     )
