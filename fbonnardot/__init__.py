#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fbonnardot: My functions (Frédéric BONNARDOT)
=============================================

Contents
--------
All fonctions of Frédéric BONNARDOT classified into thematic subpackages:

Subpackages
-----------
Importing fbonnardot imports all subpackages.

cyclostationarity
    Cyclostationary analysis of signal
detection
    Detection of peaks, ... on a signal
display
    Display utility (superposition, split into blocks, ...)
filtering
    Filtering fonctions (ekf, ...)
gui
    Various gui utilities
identification
    Identification of a filter, transfert function, ...
imagproc
    General image processing methods.
interpolation
    Interpolation methods
mechanic
    Functions to deal with gearbox, bearings, ...
sampling
    Resampling against angle, work with irregular sampling...
signalproc
    General signal processing methods
simulation
    Test signals
speed
    Estimates instantaneous speed and/or phasis
various
    Other types of functions

Note
----
Version 2020.04 01-Apr-2020
Copyright (c) 2001-2020 Frédéric BONNARDOT.

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


Warning
-------

This code is given as is without warranty of any kind.
In no event shall the authors or copyright holder be liable for any claim damages or other liability.

"""

__author__ = "Frédéric BONNARDOT"
__copyright__ = "Copyright 2020, Frédéric BONNARDOT"
__credits__ = "Frédéric BONNARDOT"
__license__ = "AGPL-3.0-or-later license"
__version__ = "2020.04d"
__maintainer__ = __author__
__email__ = "frederic.bonnardot@univ-st-etienne.fr"
__status__ = "Prototype"

from .cyclostationarity import *
from .detection import *
from .display import *
#from .filtering import * 
#from .gui import *
#from .identification import *
#from .imageproc import *
#from .interpolation import *
#from .mechanic import *
#from .sampling import *
from .signalproc import *
#from .simulation import *
from .speed import *
from .various import *
