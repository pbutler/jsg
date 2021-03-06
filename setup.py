#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: ts=4 sts=4 sw=4 tw=79 sta et
"""%prog [options]
Python source code - @todo
"""

from setuptools import setup, find_packages

setup(
    name="jsg",
    version="0.0.1",
    packages=find_packages(exclude=['tests']),
    # scripts=['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['six'],

    # package_data={
    #     # If any package contains *.txt or *.rst files, include
    #     # them:
    #     '': ['*.txt', '*.rst'],
    #     # And include any *.msg files found in the 'hello' package,
    #     # too:
    #     'hello': ['*.msg'],
    # },

    # metadata for upload to PyPI
    author="Patrick Butler",
    author_email="pbutler@killertux.org",
    description="This is an Example Package",
    # license="PSF",
    keywords="hello world example examples",
    url="http://example.com/HelloWorld/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
