#! /usr/bin/env python3

from setuptools import setup, find_packages, find_namespace_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    lic = f.read()

setup(
    name="tarstats",
    version="1.2",
    author="Kristian Köhntopp",
    author_email="kristian.koehntopp@gmail.com",
    url="https://github.com/isotopp/tarstats",
    long_description=readme,
    license=lic,
    tests_require=["pytest"],
    packages=find_packages(),
    entry_points='''
      [console_scripts]
      tarstats=tarstats:main
    ''',
)
