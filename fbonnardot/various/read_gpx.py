# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 13:50:18 2019

@author: Frédéric BONNARDOT, AGPL-3.0-or-later license
(c) Frédéric BONNARDOT, 2019-2020

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

This code is given as is without warranty of any kind.
In no event shall the authors or copyright holder be liable for any claim
                                                   damages or other liability.

If you change or adapt this function, change its name (for example add your
                                                     initial after the name)
"""

import numpy as np                       # matrix management
import lxml.objectify as objectify       # read xml (gpx) files
import datetime as dt                    # manage dates

import matplotlib.pyplot as plt

def read_gpx(path,graph=0):
    """
    Read a track from gps gpx file.

    Parameters
    ----------
    path : str
        path of gpx file.

    graph : int, optional
        1 to plot contents of gpx file, 0 otherwise

    Returns
    -------
    track : dictionary of array of float
        * lat : latitudes in degrees,
        * lon : longitudes in degrees,
        * ele : elevations in meters,
        * date : timestamps in s,
        * hr : heath rates (if avalaible) in bpm,
        * name : name of the track (str).
        
    Warning
    -------
    * Only tested with Garmin Vivoactive 2 HR
    * Parameters could evolve in the future
    
    """

    # Creation              : Monday 30 December 2019
    # Modifications         : Monday 20 April 2020 (Auto test)
    # Version               : 1.1 i

    # Open gpx file, associate to an xml reader object
    file=open(path,'r')
    parsed = objectify.parse(file)
    root = parsed.getroot()
    
    #Check that it is a gpx file
    if root.tag!='{http://www.topografix.com/GPX/1/1}gpx':
        raise ValueError(path+' is not a gpx file.')
    
    # Name of the track
    trk_name=str(root.trk.name)
    
    # Get all samples of the track
    trk_samples=root.trk.trkseg.getchildren()
    
    # Convert array of sample to arrays of latitudes, longitudes, ...
    N=len(trk_samples)
    ele=np.zeros((N))
    lat=np.zeros((N))
    lon=np.zeros((N))
    date=np.zeros((N))
    hr=np.zeros((N))
    
    for index in range(N):
        ele[index]=trk_samples[index].ele
        lat[index]=trk_samples[index].get('lat')
        lon[index]=trk_samples[index].get('lon')
        date[index]=dt.datetime.fromisoformat(str(trk_samples[index].time)[0:-1]).timestamp()
        hr[index]=trk_samples[index].extensions.getchildren()[0].hr
        
    if graph==1:
        plt.subplot(2,2,1)
        plt.plot(lat,lon)
        plt.xlabel('Latitude [degrees]')
        plt.ylabel('Longitude [degrees]')
        plt.subplot(2,2,2)
        plt.plot((date-date[0])/3600,ele)
        plt.xlabel('Time [h]')
        plt.ylabel('Elevation [m]')
        plt.subplot(2,2,4)
        plt.plot((date-date[0])/3600,hr)
        plt.xlabel('Time [h]')
        plt.ylabel('Heath rate [bpm]')
        
    return {'lat':lat,'lon':lon,'ele':ele,'date':date,'hr':hr,'name':trk_name}

# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    import os.path
    print("Auto-test if Python script launched from console")
    print("A graph with the coordinates, profile and hearth rates should be")
    print("  displayed if you give the good path.")

    path=input("Give the name of your gpx file (including the path) :")
    if (os.path.exists(path)==True):
        gps=read_gpx(path,1)
        print("Max Elevation : {:.2f}".format(np.max(gps['ele'])))
        print("Min Elevation : {:.2f}".format(np.min(gps['ele'])))
        print("Max HR : {:.1f}".format(np.max(gps['hr'])))
        print("Min HR : {:.1f}".format(np.min(gps['hr'])))
    else:
        print("The file you indicates does not exists")
