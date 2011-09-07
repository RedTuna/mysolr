# -*- coding: utf-8 -*-
from distutils.core import setup


REQUIRED = ['requests>=0.6']
CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]


setup(name='mysolr',
      version='0.1',
      description='Solr Python binding',
      long_description = open('README.rst').read(),
      author='Rubén Abad',
      author_email='ruabag@gmail.com',
      url='http://github.com/rabad/mysolr',
      packages=['mysolr'],
      install_requires=REQUIRED,
      classifiers=CLASSIFIERS)
