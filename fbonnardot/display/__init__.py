#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=======
Display
=======

Contents
--------
Functions to display data (superposition, markers, ...):

Details
-------

periodPlot
    Superpose periods of an signal in one plot
plotMatrix
    Draw an picture associated to a matrix and provide a tool to adjust visualisation
supPlot
    Display a set of signal by overlapping them
verticalLabel
    Put vertical labeled lines on the figure
 
Note
----
Version 2020.03 31-Mar-2020
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
__version__ = "2020/03"
__maintainer__ = __author__
__email__ = "frederic.bonnardot@univ-st-etienne.fr"
__status__ = "Prototype"

__all__=[
        'periodPlot',
        'plotMatrix',
        'supPlot',
        'verticalLabel'
]

from .periodPlot import periodPlot
from .plotMatrix import plotMatrix
from .supPlot import supPlot
from .verticalLabel import verticalLabel