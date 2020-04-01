#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====
Speed
=====

Contents
--------
Functions to estimate instantaneous speed and/or phasis.

Details
-------

demodAnalytic
    Retreive the phase and the frequency by using the analytic signal phase
    around a given frequency band.
synchronisation2
    Synchronisation of data by using intercorrelation or an amplitude based detection.

Note
----

Version 2020.04 01-Apr-2020
Copyright (c) 2001-2020 Frédéric BONNARDOT.
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/
 
Warning
-------

This code is given as is without warranty of any kind.
In no event shall the authors or copyright holder be liable for any claim damages or other liability.

"""

__author__ = "Frédéric BONNARDOT"
__copyright__ = "Copyright 2020, Frédéric BONNARDOT"
__credits__ = "Frédéric BONNARDOT"
__license__ = "CC BY-NC-SA 4.0"
__version__ = "2020.04"
__maintainer__ = __author__
__email__ = "frederic.bonnardot@univ-st-etienne.fr"
__status__ = "Prototype"

__all__ = [
        'synchronisation2',
        'demodAnalytic'
]

from .demodAnalytic    import demodAnalytic
from .synchronisation2 import synchronisation2