#!/usr/bin/env python

from setuptools import setup


setup(
    name="xrdpattern",
    version="1.0",
    py_modules=["xrdpattern"],
    entry_points={
        "console_scripts": ["xrdpattern = xrdpattern:main"],
    },
)
