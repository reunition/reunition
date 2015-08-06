#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import reunition

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = reunition.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='reunition',
    version=version,
    description="""Django project for running a reunion planning website""",
    long_description=readme + '\n\n' + history,
    author='Elevencraft Inc.',
    author_email='matt+reunition@11craft.com',
    url='https://github.com/reunition/reunition',
    packages=[
        'reunition',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='reunition',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
