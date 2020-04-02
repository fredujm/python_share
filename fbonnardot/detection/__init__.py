#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========
Detection
=========

Contents
--------
Methods for detection:

Details
-------

peakDetection
     Detect peaks in a signal
globalMinMax
     Detection of locals minimum and maximum.
 
Note
----
Version 2019.04 01-Apr-2020
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
__version__ = "2020.04"
__maintainer__ = __author__
__email__ = "frederic.bonnardot@univ-st-etienne.fr"
__status__ = "Prototype"

__all__=[
        'peakDetection',
        'globalMinMax'
]

from .globalMinMax  import globalMinMax
from .peakDetection import peakDetection
