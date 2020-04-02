#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 15:40:02 2018

@author: Frédéric BONNARDOT, AGPL-3.0-or-later license
(c) Frédéric BONNARDOT, 2001-2020

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
import scipy.interpolate as interp       # interpolation
import warnings
import matplotlib.pyplot as plt          # Plot
#from .supPlot import supPlot
import fbonnardot.display.supPlot

plt.rcParams['toolbar'] = 'toolmanager'  # Pour ajouter une toolbar

def periodPlot(data,period,selection=0,moments=0,orient='vert',overlap=0,Ts=1,scale='ind',axes=None,line_opts=None):
    """
    Superpose periods of an signal in one plot
    
    Parameters
    ----------
    data : vector (np.array)
        Datas to plot
        
    period : integer or float
        period of the data to plot
        if the period is not integer, an resampling will be done before splitting the datas
        
    selection : integer or vector, optionnal
        - if integer  :
              - 0 for showing all periods
              - n for showing the period no. n^i
              - -n for automatic selection (n biggest difference with the synchronous averaging).
        - if vector  : periods to plot
        optionnal, 0 by default
        
    moments : integer, optionnal
        - 0 to display no moments
        - 1 for synchronous average (on top)
        - n for the n first moments (on top the higher curve is the n moment)
        - -n for the cumulant of n order limited to n<=4
        optionnal, 0 by default
        
    orient : string, optionnal
        Angle of the name of the signals
            - 'horiz' : for horizontal
            - 'vert'  : for vertical
            - 'no'    : no signal name and block n° displayed
        optionnal, 'vert' by default
        
    overlap : integer, optionnal
        Overlap between signals
            - 0   by default
            - -1 for superposing the signals
        optionnal, 0 by default
        
    Ts : float, optionnal
        Sampling period
        optional, 1 by default
        
    scale : string, optionnal
        Scale of signals
            - 'ind' : each signal have its own scale to fit in the n, n+1 box
            - 'glo' : same scale for each signal
        optionnal, 'ind' by default
        
    axes : object, optionnal
        Axes to draw the datas or None to use current Axes
        optionnal, None by default
        
    line_opts : string, optionnal
        display extra curves for each lines
        optional, None by default
            - 'min'     : add minimum value
            - 'max'     : add maximum value
            - 'm3sigma' : add average-3.standard deviation
            - 'p3sigma' : add average+3.standard deviation
            - 'mean'    : add average value
               
    Returns
    -------
    array1 : vector or scalar
            - 0 if moments=0
            - mean and power of each moments if moments~=0
        in the form [mean1 power1;mean2 power2;...]
    array2 : vector
        moments or cumulants or 0
    
    Note
    ----
    The first period is period n°1
    
    Examples
    --------

    >>> import fbonnardot as fb; import numpy as np
    >>> N=1000; t=np.arange(N); period=30.223
    >>> signal=np.sin(2*np.pi*t/period)+0.1*np.random.randn(N)
    >>> fb.periodPlot(signal,period,2,2)
    
"""    
    
    # Creation              : Thursay 12 July 2001       (MATLAB version)
    # Modifications         : Wednesday 26 December 2018 (Translation to Python 3.6)
    #                         Monday 9 December 2019 (Add axes parameter)
    #                         Monday 30 December 2019 (Add line_opts parameter) 
    #                         Thursday 6 February 2020 (orient='no' option)
    #                         Tuesday 31 March 2020 (NumPy docstring - autotest)
    # Version               : 1.82 i

    # Check parameters
    if np.isscalar(selection):
        if selection==1:
            raise ValueError('Selection can\'t be 1 : 1^i=1 for all i !')

    if abs(moments)>4:
        raise ValueError('Limited to 4th order statistics.')

    if period<0:
        raise ValueError('A period can''t be negative.')
        
    if len(data)<2*period:
        raise ValueError('You need at least 2 periods.')

    if (abs(overlap)>=1 or abs(overlap)<0) and overlap!=-1:
        raise ValueError('Overlap must be in [0;1[.')
        
    names=[]
    m=None
    puiss=None

    # Case of non integer periods
    if type(period) is not int:
        warnings.warn('Not an integer period => resampling.')
        N=len(data)
        step=period/np.ceil(period)
        int_func=interp.interp1d(np.arange(1,N+1,1),data,'cubic')
        data_int=int_func(np.arange(1,N,step))
        return periodPlot (data_int,int(np.ceil(period)),selection,moments,orient,overlap,Ts/step,scale,axes,line_opts)
    else:
        # Split datas
        occurences=int(np.floor (len (data) / period))
        if occurences!=len (data)/period:
            warnings.warn ('Not a integer number of period, the last period was suppressed.')

        t=range(int(occurences*period))
        blocks=np.reshape (data[t],(occurences,period))

        # Choix of displayed blocks
        if np.isscalar(selection):
            # Scalar case for selection
            if selection==0:
                # Display all blocks
                disp_index=np.arange(occurences)
                for i in range(occurences):
                    names.append(str(i+1))
            elif selection>0:
                # selection scalar>0 => display period n° selection^i   
                nb_elem=int(np.floor(np.log(occurences)/np.log(selection))+1)
                #disp_blks=np.zeros((period,nb_elem))
                disp_index=np.zeros(nb_elem,dtype=int)
                puissanceI=1
                for i in range(nb_elem):
                    disp_index[i]=int(np.floor(puissanceI-1))
                    names.append(str(int(np.floor(puissanceI))))
                    puissanceI=puissanceI*selection
            else:
                # selection scalar<0 => automatic choice of period to display
                # computes synchronous average
                msync=np.mean(blocks,1)
                # computes residual energy for each cycle
                energy=np.zeros(occurences)
                for cycle in range(occurences):
                    # compute the residual
                    vecart=blocks[:,cycle]-msync
                    # and its energy
                    energy[cycle]=np.sum(vecart*vecart)
                # sort the energy by decreasing order - retreive the indices
                order=np.argsort(-energy)
                # keep the -selection greater
                nb=min (-selection,len(energy))
                i=np.arange(nb)
                disp_index=order[i]
                for i in range(nb):
                    names.append(str (order[i]+1))
        else:
            selection=np.array(selection)-1
            # Selection by using a vector
            if np.max(selection)>=occurences or np.min(selection)<0:
                # We do not have all asked periods - find which one
                notok=np.where(np.logical_or(selection>occurences,selection<0))[0]
                for per in notok:
                    warnings.warn('The period '+str(per)+' is not in the signal.')                  
            ok=np.where(np.logical_and(selection<occurences,selection>=0))[0]
            # Select the avalaible periods
            disp_index=selection[ok]

            for i in range(len (ok)):
                names.append(str (selection[ok[i]]+1))
    
    if line_opts!=None:
        tlo=1 # Number of elements per lines
        fmt=['k']
        if 'min' in line_opts:
            tlo=tlo+1
            fmt.append('b')
        if 'm3sigma' in line_opts:
            tlo=tlo+1
            fmt.append('b')
        if 'max' in line_opts:
            tlo=tlo+1
            fmt.append('r')
        if 'p3sigma' in line_opts:
            tlo=tlo+1
            fmt.append('r')
        if 'mean' in line_opts:
            tlo=tlo+1
            fmt.append('k--')
            
        #  sig nb in stack x stack x period
        disp_blks=np.zeros((tlo,len(disp_index),period))
        for st in range(len(disp_index)):
            if st==len(disp_index)-1:
                local_blks=blocks[disp_index[-1]:,:]
            else:
                local_blks=blocks[disp_index[st]:disp_index[st+1],:]

            # Display asked period
            disp_blks[0,st,:]=local_blks[0]
            tlo=1
            
            if 'min' in line_opts:
                disp_blks[tlo,st,:]=np.min(local_blks,axis=0)
                tlo=tlo+1
            if 'm3sigma' in line_opts:
                disp_blks[tlo,st,:]=np.mean(local_blks,axis=0)-3*np.std(local_blks,axis=0)
                tlo=tlo+1
            if 'max' in line_opts:
                disp_blks[tlo,st,:]=np.max(local_blks,axis=0)
                tlo=tlo+1
            if 'p3sigma' in line_opts:
                disp_blks[tlo,st,:]=np.mean(local_blks,axis=0)+3*np.std(local_blks,axis=0)
                tlo=tlo+1
            if 'mean' in line_opts:
                disp_blks[tlo,st,:]=np.mean(local_blks,axis=0)
                tlo=tlo+1
    else:
        disp_blks=blocks[disp_index,:]
        fmt='k'

    # Statistics (mean, cumulants, ...)
    if moments!=0:
        # Computes moments
        m=np.zeros((abs(moments),period))
        for mom in range(abs(moments)):
            m[mom,:]=np.mean(blocks**(mom+1),0)

        if moments<-1:
            # Computes cumulants
            if moments==-4:
                m[3,:]=cumulant4 (m [0,:],m [1,:],m [2,:],m [3,:])
            if moments<=-3:
                m[2,:]=cumulant3 (m [0,:],m [1,:],m [2,:])
            if moments<=-2:
                m[1,:]=cumulant2 (m [0,:],m [1,:])

        # legende
        if abs(moments)>0:
            names.append('s.av')

        if moments>1:
            for i in np.arange(2,moments+1):
                names.append('mom. '+str(i))
        elif moments<1:
            names.append('svar')
            for i in np.arange(3,-moments+1):
                names.append('cum. '+str(i))

        [li,col]=disp_blks.shape[-2:]
        i=np.arange(li+1,li+1+abs (moments))
        if line_opts==None:
            disp_blks=np.append(disp_blks,m,axis=0)
        else:
            disp_blks=np.append(disp_blks,np.tile(m,(tlo,1,1)),axis=1)
        puiss=np.zeros((abs(moments),2))
        for moy in range(abs (moments)):
            puiss[moy,0]=np.mean(m[moy,:])      
            puiss[moy,1]=np.var (m[moy,:])

    # Call supplot for display
    [li,col]=disp_blks.shape[-2:]

    fbonnardot.display.supPlot (disp_blks,col,0,Ts,names,orient,overlap,scale,axes,fmt=fmt)
    if orient!="no":
        if axes==None:
            plt.text (0,1,str(li)+' blocks   ', ha='right',va='bottom')
        else:
            axes.text (0,1,str(li)+' blocks   ', ha='right',va='bottom')

    return puiss,m

# Compute cumulants
# See the book  "Le signal aléatoire" p.52 of D. Declercq, A. Quinquis - Hermes

def cumulant4 (m1,m2,m3,m4):
    return m4-4*m1*m3-3*m2*m2+12*m1*m1*m2-6*m1*m1*m1*m1

def cumulant3 (m1,m2,m3):
    return m3-3*m1*m2+2*m1*m1

def cumulant2 (m1,m2):
    return m2-m1*m1

# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    print("Auto-test if Python script launched from console")
    print("You should see a graph with a stack of noise + sine wave, synchronous average and variance.")
    N=1000; t=np.arange(N); period=30.223
    signal=np.sin(2*np.pi*t/period)+0.1*np.random.randn(N)
    periodPlot(signal,period,2,2)
    