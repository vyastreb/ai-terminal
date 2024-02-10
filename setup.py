#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib as pl
from setuptools import setup, find_packages
import ai_terminal as ait

name = 'ai-terminal'
contact = "xxx"
version = ait.__version__

here = pl.Path(__file__).parent.absolute()

requirements = []
with open(here / pl.Path("requirements.txt")) as fid:
    content = fid.read().split("\n")
    for line in content:
        if line.startswith("#") or line.startswith(" ") or line == "":
            continue
        elif line.startswith("-e"):
            pname = line.split("#egg=")[1]
            req_line = "{} @ {}".format(pname, line[3:])
            requirements.append(req_line)
        else:
            requirements.append(line)

with open(here / pl.Path("README.md")) as fid:
    long_description = fid.read()

setup(
    name=name,
    version=version,
    author_email=contact,
    description="Interface to interact with a chatbot in Linux terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD-3-Clause license",
    url="",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering'
    ],
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
    entry_points = {
        'console_scripts': ['ai=ai_terminal:entry_point'],
    }
)