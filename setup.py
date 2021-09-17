#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup


setup(
    author="AI2 Climate Modelling",
    author_email="tobiasw@allenai.org",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    description="AI2 DSL internal performance analysis and vizualization",
    extras_require={},
    license="BSD license",
    include_package_data=True,
    name="perfviz",
    packages=find_packages(include=["."]),
    setup_requires=[],
    version="0.0.0",
    zip_safe=False,
)
