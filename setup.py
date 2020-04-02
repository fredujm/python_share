#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:35:02 2020

@author: Frédéric BONNARDOT, AGPL-3.0-or-later license

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

This file was created by using the tutorial at
http://sametmax.com/creer-un-setup-py-et-mettre-sa-bibliotheque-python-en-ligne-sur-pypi/
"""

from setuptools import setup, find_packages
 
import fbonnardot
 
setup(
 
    # Name of library for pypi
    name='fbonnardot',
 
    # Version of code
    version=fbonnardot.__version__,
 
    packages=find_packages(),
 
    author=fbonnardot.__author__,
 
    author_email=fbonnardot.__email__,
 
    # Short description
    description="Signal processing tools for Python.",
 
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
 
    # Packages needed
    install_requires= ["numpy","scipy","matplotlib","PyQt5"],
 
    # Use file MANIFEST.in
    include_package_data=True,
 
    # Link with github page
    url='https://github.com/fredujm/python_share',
 

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering"],
 
 
 
    # A fournir uniquement si votre licence n'est pas listée dans "classifiers"
    # ce qui est notre cas
    license="GNU Affero General Public License v3 or later (AGPLv3+)",

 
)