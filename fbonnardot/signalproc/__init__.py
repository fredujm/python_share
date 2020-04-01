#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================
Signal Processing
=================

Contents
--------
General signal processing methods.

Details
-------

circShift
    Circular shift of datas (use a Fourier Transform if shift is not an integer).

Note
----

Version 2019.02 03-Feb-2019
Copyright (c) 2001-2020 Frédéric BONNARDOT.
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
 
Warning
-------

This code is given as is without warranty of any kind.
In no event shall the authors or copyright holder be liable for any claim damages or other liability.

"""

__author__ = "Frédéric BONNARDOT"
__copyright__ = "Copyright 2019, Frédéric BONNARDOT"
__credits__ = "Frédéric BONNARDOT"
__license__ = "CC BY-NC-SA 4.0"
__version__ = "2020.04"
__maintainer__ = __author__
__email__ = "frederic.bonnardot@univ-st-etienne.fr"
__status__ = "Prototype"

__all__ = [
        'circShift'
]

from .circShift import circShift

