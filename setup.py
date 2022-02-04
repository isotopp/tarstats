#! /usr/bin/env python3

from setuptools import setup

setup(
    name="tarstats",
    version=1.0,
    py_modules = [ "tarstats"],
    install_requires = [ "Click"],
    entry_points = '''
      [console_scripts]
      tarstats=tarstats:tarstats
    ''',
)
