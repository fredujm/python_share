#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:35:02 2020

@author: Frédéric BONNARDOT, CC BY-NC-SA 4.0 license

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/

This code is given as is without warranty of any kind.
In no event shall the authors or copyright holder be liable for any claim
                                                   damages or other liability.

If you change or adapt this function, change its name (for example add your
                                                       initial after the name)

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
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering"],
 
 
 
    # A fournir uniquement si votre licence n'est pas listée dans "classifiers"
    # ce qui est notre cas
    license="Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License",

 
)