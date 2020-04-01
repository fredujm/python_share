#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:44:43 2019

@author: Frédéric BONNARDOT, CC BY-NC-SA 4.0 license

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/

This code is given as is without warranty of any kind.
In no event shall the authors or copyright holder be liable for any claim
                                                   damages or other liability.

If you change or adapt this function, change its name (for example add your
                                                       initial after the name)
"""

import numpy             as np                 # matrix management
import scipy.interpolate as interp             # interpolation

def peakDetection (signal,method='kStdThreshold',k=3,Nmax=np.Inf,k2=None):
    """
    Detect peaks in a signal
    
    Parameters
    ----------
    
    signal : vector
        signal
        
    method : string, optionnal
        - 'kStdThreshold' : use a threshold=k*std(signal) and return the Nmax
            biggest values
        - 'diff' : differenciate the signal and look at sign changes (+ to -)
        - 'diffInterp' : differenciate the signal and look at sign changes (+ to -)
            use interpolation to find accurate results
        optionnal, by default method='kStdThreshold'
 
    k : scalar, optionnal
        meaning depends of the method used
            - 'kStdThreshold' : coefficient for selection
            - 'diff'          : minimum spacing between peaks
        optionnal, k=3 by default
                                   
    Nmax : integer, optionnal
        maximum number of peaks to be detected
        optionnal, Nmax=Inf by default
 
    k2 : integer, optionnal
        - for 'kStdThreshold' : minimum spacing between peaks,
            optionnal, k=1 by default
        - for 'diffinterp' : interpolation factor
            optionnal, 4 by default
 
    Return
    ------
    position : vector
        peaks position
        
    amp : vector
        amplitude of signal signal at peaks position
        
    Example
    -------
    >>> import fbonnardot as fb; import matplotlib.pyplot as plt
    >>> import scipy.signal as sigp; import numpy as np
    >>>
    >>> # Generate test signal
    >>> timp=np.array(np.cumsum(np.random.rand(30)*10+1000),int)-500
    >>> signal=np.zeros(int(max(timp))+500)
    >>> signal[timp]=3+np.random.randn(len(timp))*0.2
    >>> signal=sigp.lfilter([1],[1,0.9],signal); signal+=np.random.randn(len(signal))*0.03
    >>> #plt.figure(); plt.plot(signal)
    >>> signal=sigp.decimate(signal,10)
    >>> b,a=sigp.butter(3,2*6.28/100)
    >>> signal2=sigp.filtfilt(b,a,signal)
    >>>
    >>> positionts1,ampts1=fb.peakDetection(signal,'kStdThreshold')
    >>> positionds1,ampds1=fb.peakDetection(signal,'diff',Nmax=40)
    >>> positionts2,ampts2=fb.peakDetection(signal2,'kStdThreshold')
    >>> positionds2,ampds2=fb.peakDetection(signal2,'diff',Nmax=40)
    >>>
    >>> # Graphs
    >>> plt.figure()
    >>> plt.subplot(2,1,1)
    >>> plt.plot(signal)
    >>> plt.plot(positionds1,ampds1,'o')
    >>> plt.plot(positionts1,ampts1,'x')
    >>> plt.subplot(2,1,2)
    >>> plt.plot(signal2)
    >>> plt.plot(positionds2,ampds2,'o')
    >>> plt.plot(positionts2,ampts2,'x')
    >>> plt.legend(['signal','diff method','threshold method'])


    Note
    ----
    * NaN and Inf are not considered as peaks
    * Outputs vector are sorted by amplitude descending order
    """

    # Creation              : Monday 26 May 2003 (MATLAB version)
    # Modifications         : Friday 1st February 2019 (Translation to Python 3.6)
    #                         Thursay 12 December 2019 (Correct bug in peakSelection)
    #                         Tuesday 17 December 2019 (Change algorithm for peakSelection)
    #                                                  (Add progress bar)
    #                         Wednesday 1st April 2020 (Auto-test, example and Numpy Docstrings)
    # Version               : 1.2 i

    # Check arguments
    if method not in ('kStdThreshold','diff','diffInterp'):
        raise ValueError('Illegal value for method.')
    
    if k2==None:
        if method=='kstdthreshold':
            k2=1
        else:
            k2=4
    
    # Remove NaN and Inf
    signal=np.array(signal) # Work on a copy of signal
    ok=np.where(np.isfinite(signal))[0]
    pb=np.where(np.isfinite(signal)==False)[0]
    signal[pb]=np.min(signal[ok])
    
    # Choose method
    if method=='kStdThreshold':
        return kStdThreshold (signal,k,Nmax,k2)
    elif method=='diff':
        return diffmethod    (signal,k,Nmax)
    elif method=='diffInterp':
        return diffinterp    (signal,k,Nmax,k2)       

    
def kStdThreshold (signal,k,Nmax,mindist):
    
    # Detection of low probabilistic values according to a Gaussian low
    m=np.mean(signal)
    signal=signal-m
    threshold=np.std(signal)*k
    pos=np.where(signal>threshold)[0]
    amp=signal[pos]
    
    # Sort this values by descending order
    #[order,permutation]=sort(amp.*-1);
    #pos=pos(permutation);
    
    # Limitation to Nmax values
    #if length(position)>Nmax
    #    position=position(1:Nmax);
    #end;
    position=peakSelection (pos,amp,Nmax,mindist)
    
    amp=signal[position]+m
    
    return position,amp
    

    
def diffmethod (signal,mindist,Nmax):
    
    if mindist<=0:
        raise ValueError('The minimum distance beetween peaks cannot be 0 or negative.')
    
    N=len(signal)
    m=min(signal)
    
    # Find peak location and value by differenciation
    deriv=np.diff(np.concatenate(([m] , signal , [m])))
    pos=np.where(np.logical_and(deriv[0:N]>=0,deriv[1:N+1]<=0))[0]
    amp=signal[pos]
    
    # Peak selection
    position=peakSelection (pos,amp,Nmax,mindist)
    amp=signal[position]
    
    return position,amp
    
    
def diffinterp (signal,mindist,Nmax,ifactor):
    
    #%signal=resample (signal,ifactor,1);
    #%[position,amp]=diffmethod (signal,mindist,Nmax);
    #%position=position./ifactor;
    
    # Use classic method to find position
    position,amp=diffmethod (signal,mindist,Nmax)
    
    N=len (signal)
    
    # Refine each position
    delta=np.arange(-10,11)
    for index in range(len(position)):
        pos=position[index]
        if pos>4 and pos<(N-6):
            fx=interp.interp1d(delta,signal[pos+delta])
            y=fx(np.arange(-ifactor,ifactor+1)/ifactor)
            delta=np.argmax(y)
            position[index]=pos+(delta-ifactor-1)/ifactor
            
    return position,amp



def peakSelection (pos,amp,Nmax,mindist):
    """
    Selection Nmax higher peaks from the list and ignore close peaks (close mean <mindist)
    
    Input
    -----
    pos     : position of the peaks
    amp     : amplitude of the peaks
    Nmax    : maximum number of peaks to select
    mindist : minimum distance between peaks
    
    Return
    ------
    pos     : selected peaks position
    """
    
    # Sort positions by decreasing amplitudes
    asrt=np.argsort(-amp)
    pos=pos[asrt]
    # Go from highest to lowest amplitude to remove close peaks
    n=0
    while n<Nmax and len(pos)>n:
        NN=np.min((Nmax,len(pos)))
        progressBar(n/NN)
        # Remove close peaks
        dist=np.abs(pos-(pos[n]))
        dist[n]=mindist+1 # To keep current at a dist=0
        farp=np.nonzero(dist>=mindist)[0] # remove when dist<mindist
        pos=pos[farp]
        # Go to next value
        n=n+1

    progressBar(-1)
    
    return np.sort(np.array(pos[0:n]))

def progressBar(position):
    """
    Display a text progress bar
    
    Parameters
    ----------
    
    position   : between 0 and 1
                 otherwise suppress the bar
    """
    
    if position>=0 and position<=1:
        nb_done=int(np.ceil(position*50))
        print("\rpeakDetection : \u001b[44;1m"+">"*nb_done+"\u001b[0m\u001b[44m"+"-"*(50-nb_done)+"\u001b[0m",end='')
    else:
        print("\r"+" "*70+"\r\u001b[A")
        
# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    import scipy.signal as sigp; import matplotlib.pyplot as plt
    print("Auto-test if Python script launched from console")
    print("You should see two sub figures.")
    print("Figure 1 : a noisy signal with peaks. Peak are marked with a cross and round.")
    print("Figure 2 : low pass filtered version with peak detection.")

    # Generate test signal
    timp=np.array(np.cumsum(np.random.rand(30)*10+1000),int)-500
    signal=np.zeros(int(max(timp))+500)
    signal[timp]=3+np.random.randn(len(timp))*0.2
    signal=sigp.lfilter([1],[1,0.9],signal); signal+=np.random.randn(len(signal))*0.03
    #plt.figure(); plt.plot(signal)
    signal=sigp.decimate(signal,10)
    b,a=sigp.butter(3,2*6.28/100)
    signal2=sigp.filtfilt(b,a,signal)
    
    positionts1,ampts1=peakDetection(signal,'kStdThreshold')
    positionds1,ampds1=peakDetection(signal,'diff',Nmax=40)
    positionts2,ampts2=peakDetection(signal2,'kStdThreshold')
    positionds2,ampds2=peakDetection(signal2,'diff',Nmax=40)
    
    # Graphs
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(signal)
    plt.plot(positionds1,ampds1,'o')
    plt.plot(positionts1,ampts1,'x')
    plt.subplot(2,1,2)
    plt.plot(signal2)
    plt.plot(positionds2,ampds2,'o')
    plt.plot(positionts2,ampts2,'x')
    plt.legend(['signal','diff method','threshold method'])
    