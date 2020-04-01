#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 17:54:47 2019

@author: Frédéric BONNARDOT, CC BY-NC-SA 4.0 license

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/

This code is given as is without warranty of any kind.
In no event shall the authors or copyright holder be liable for any claim
                                                   damages or other liability.

If you change or adapt this function, change its name (for example add your
                                                       initial after the name)
"""

import numpy as np                       # matrix management
import matplotlib.pyplot as plt          # plot
import scipy.signal as sig               # Signal processing fonctions
import warnings

def globalMinMax (datas,method='savgol',pmeth=None,badrem='period',enh=None,penh=None,graph=0):
    """
    Detection of locals minimum and maximum.

    Parameters
    ----------
    datas : matrix or vector,
        - nb_sig signals of N samples stored in column (Nxnb_sig matrix)
        - or vector if only one signal
                    
    method : string, optionnal
        method to extimate min and max location
            - 'diff' : use diff to estimate the 1st and 2nd derivative
            - 'poly' : use a local polynomial regression to estimate the derivative
                be careful, 1 polynomial is estimated per sample
            - 'savgol' : use Savitzky-Golay to estimate the local polynomial
                approx. 100 times faster than poly
        optional, savgol by default
                  
    pmeth : string, optionnal
        parameters for method
            - 'diff' : None (no parameter required)
            - 'poly' : 2 elements [delta,order] where
                - order is the polynomial order
                - 2*delta+1 is the number of samples used for regression
                         if value is None, use [10;2]
            - 'savgol' : same as poly
        optional, None by default
                  
    badrem : string, optionnal
        enable to suppress false detection
            - None : no false detection suppression
            - 'period' : compute distance between consecutive mininums
                partition this distance in two groups (false and exact)
                remove points associated in false group
                next do the same for maximums
        optional, 'period' by default
                  
    enh : string, optionnal
        enhance position detection of minimum and maximum
        tupple of two value to set up pmin and pmax
            or one value to apply to pmin and pmax
        - None     : no enhancement
        - 'zak'    : method proposed by F. Zakaria in its thesis
                       start with  given minimum
                       compare with delta next samples
                         minimum if the serie is ascending without descending
                         else update minimum position to the left reiterate
                        ascending or descending is evaluated with the derivative
                        estimated previously
        optional, None by default
                  
    penh : string, optionnal
        parameter or tuple of parameter for enh
            - 'zak' : give value of delta, if None delta is set to 30
        optional, None by default

    graph : scalar,
        - 1 to display a figure to show the result (only if nb_sig=1)
        - 0 else
        optional, 0 by default
            
    Return
    ------
    pmin : array
        - array of containing nb_sig arrays of minimum positions
        - or just an array of minimum position if datas is a vector
    
    pmax : array
        - array of containing nb_sig arrays of maximum positions
        - or just an array of minimum position if datas is a vector

    Example
    -------
    >>> import fbonnardot as fb; import numpy as np; import scipy as sp
    >>> pvar=100; pmin=20; data=np.array([])
    >>> for it in range(10):
    >>>     data=np.concatenate([data,np.ones(int(np.random.rand()*pvar)+pmin),
                    np.ones(int(np.random.rand()*pvar)+pmin)*-1])
    >>> dataf=sp.signal.lfilter([1,0],[1,-np.exp(-2*np.pi/30)],data)+np.random.randn(len(data))*0.1
    >>> pmin,pmax = fb.globalMinMax (dataf,enh='zak',graph=1)

    Note
    ----
    For method 'diff' and 'poly' :
        - a maximum local is detected when derivative goes from - to + and
             amplitude of data is greater than 0.3 (on normalized data)
        - a maximum local is detected when derivative goes from - to + and
             amplitude of data is lower than 0.7 (on normalized data)
             
    Bibliography
    ------------
    - https://fr.wikipedia.org/wiki/Algorithme_de_Savitzky-Golay
    - Abraham Savitzky et Marcel J. E. Golay, « Smoothing and Differentiation of Data by Simplified Least Squares Procedures », Analytical Chemistry, vol. 8, no 36,‎ 1964, p. 1627–1639 (DOI 10.1021/ac60214a047)
    - Human locomotion analysis : exploitation of cyclostationarity properties of signals, F. Zakaria (http://www.theses.fr/2015STET4019)
    """
    
    # Creation              : Friday 2 September 2016 (MATLAB version)
    # Modifications         : Monday 15 January 2018  (Translation to Python 3.6)
    #                         Thursday 31 January 2018 (in enhance detection
    #                            remove close samples instead of remove identical samples)
    #                         Wednesday 1st April 2020 (Docstrings and auto-test)
    # Version               : 1.0 i

    def part_2 (signal,nb_iter,min_s):
        """ Partition in 2 clusters signal with min and max as initial position
               next, update position of the 2 clusters (k-means)
            If a cluster have less than t_min elements, suppress elements from
               the set and try again
        """
        ec1=np.min(signal); ec2=np.max(signal);

        iter=0
        while iter<nb_iter:
            center=(ec1+ec2)/2
            pc1=np.where(signal<center)[0]; pc2=np.where(signal>center)[0]
            # Is the number of elements of cluster significant ?
            if len(pc1)>min_s and len(pc2)>min_s:
                # Update the center of clusters
                ec1=np.mean(signal[pc1]); ec2=np.mean(signal[pc2])
            else:
                # A cluster have non significative element-> suppress them
                if len(pc1)<=min_s:
                    signal=signal[pc2]
                else:
                    signal=signal[pc1]
                ec1=np.min(signal); ec2=np.max(signal);
                iter=iter-1 # Cancel iteration
            iter=iter+1
        
        return ec1,ec2
    
    ########

    if np.ndim(datas)>1:
        # Case where datas is a matrix => call nsig time this algo with vector datas
        N,nb_sig = datas.shape
        if nb_sig>N:
            warnings.warn ('Be careful : it seems that you have transposed datas (number of signals>signal size) !')
        pmin=[]
        pmax=[]
        for index in range(nb_sig):
            lpmin,lpmax=globalMinMax(datas[:,index],method,pmeth,badrem,enh,penh,0)
            pmin.append(lpmin)
            pmax.append(lpmax)

        return pmin, pmax
    
    N=len(datas)

    if pmeth==None and (method=='poly' or method=='savgol'):
        pmeth=[10,2]

    if type(enh) is not list and type(enh) is not tuple:
        enh=(enh,enh)

    if type(penh) is not list and type(penh) is not tuple:
        penh=(penh,penh)
    
    
    # Normalization of signal between 0 and 1 :
    #   we work in area 0.1 N to 0.9 N to be protected of border effect
    nn=np.arange(int(0.1*N),int(0.9*N))
    vmax=np.max(datas[nn])
    vmin=np.min(datas[nn])
    
    data_norm=(datas-vmin)/(vmax-vmin)
    
    # Search of minimum and maximum
    
    # Derivative bases method
    if method=='poly' or method=='diff' or method=='savgol':
        if method=='diff':
            deriv =np.concatenate([np.diff(data_norm), [0]])
            #deriv2=np.concatenate([np.diff(deriv)    , [0]])
        elif method=='poly':
            # Polynomial fit and deduce derivative
            delta=pmeth[0]
            order=pmeth[1]
            deriv =np.zeros(N)
            #deriv2=np.zeros(N)
            # At the begining we do not have delta previous samples -> we do our best
            for index in range(delta):
                # Use x=0 where we want to compute the derivative
                coeffs=np.polyfit(np.arange(-index,delta+1),data_norm[0:index+delta+1],order)
                deriv [index]=coeffs[-2]
                #deriv2[index]=coeffs[-3]/2
            # After we can compute using sampled before and after
            for index in range(delta,N-delta):
                coeffs=np.polyfit(np.arange(-delta,delta+1),data_norm[np.arange(index-delta,index+delta+1)],order)
                deriv [index]=coeffs[-2]
                #deriv2[index]=coeffs[-3]/2
            # At the end, some coefficient after are also missing
            for index in range(N-delta,N):
                coeffs=np.polyfit(np.arange(-delta,N-index),data_norm[np.arange(index-delta,N)],order)
                deriv [index]=coeffs[-2]
                #deriv2[index]=coeffs[-3]/2
        elif method=='savgol':
            # Polynomial fit and deduce derivative
            delta=pmeth[0]
            order=pmeth[1]
            deriv =sig.savgol_filter(data_norm,2*delta+1,order,deriv=1)
            #deriv2=sig.savgol_filter(data_norm,2*delta+1,order,deriv=2)
    
        # For each methods based on derivative
        # Find extremum by zero crossing detection
        t=np.arange(0,N-1)
        pmax=2+np.where(np.logical_and(np.logical_and(deriv[t]>=0,deriv[t+1]<0),data_norm[t]>0.3))[0]
        pmin=2+np.where(np.logical_and(np.logical_and(deriv[t]<0,deriv[t+1]>=0),data_norm[t]<0.7))[0]
    else:
        raise ValueError('Unknown method')
    
    # Suppress false detection
    if badrem=='period':
        # Compute the "period" between 2 minimum and partition in 2 groups
        ecart=np.diff(pmin)
        ec1,ec2=part_2(ecart,nb_iter=3,min_s=int(np.ceil(len(ecart)/10)))
        # Filter if ec1<0.5 ec2 (i.e. there is 2 distinct periods)
        if ec1<0.5*ec2:
            center=(ec1+ec2)/2
            pok=1+np.where(ecart>=center)[0]
            pmin=pmin[pok]
        # Same for pmax
        ecart=np.diff(pmax)
        ec1,ec2=part_2(ecart,nb_iter=3,min_s=int(np.ceil(len(ecart)/10)))
        if ec1<0.5*ec2:
            center=(ec1+ec2)/2
            pok=1+np.where(ecart>=center)[0]
            pmax=pmax[pok]
    elif badrem!=None:
        raise ValueError ('Unknown method for badrem')
            
    # Enhance detection
    if enh[0]=='zak':
        deltaz=penh[0]
        if deltaz==None:
            deltaz=30
        for it in range(len(pmin)):
            pos=pmin[it]
            t=np.arange(pos,min(N-1,pos+deltaz))
            while np.count_nonzero(deriv[t]<0)!=0 and pos+deltaz<N-1:
                pos=pos+1
                t=np.arange(pos,min(N-1,pos+deltaz))
            pmin[it]=pos
        # Remove close values (i.e. a position that differs of more than 4 samples)
        pmin=pmin[np.where(np.diff(pmin)>4)[0]]
    elif enh[0]!=None:
        raise ValueError('Unknown method for enh')
        
    # Enhance detection
    if enh[1]=='zak':
        deltaz=penh[1]
        if deltaz==None:
            deltaz=30
        for it in range(len(pmax)):
            pos=pmax[it]
            t=np.arange(pos,min(N-1,pos+deltaz))
            while np.count_nonzero(deriv[t]>0)!=0 and pos+deltaz<N-1:
                pos=pos+1
                t=np.arange(pos,min(N-1,pos+deltaz))
            pmax[it]=pos
        # Remove close values (i.e. a position that differs of more than 4 samples)
        pmax=pmax[np.where(np.diff(pmax)>4)[0]]
    elif enh[1]!=None:
        raise ValueError('Unknown method for enh')
    
    if graph==1:
        plt.plot(datas,'k')
        if method=='diff' or method=='poly' or method=='savgol':
            plt.plot(deriv,'g')
        plt.plot(pmax,datas[pmax],'or')
        plt.plot(pmin,datas[pmin],'ob')
        if method=='diff' or method=='poly' or method=='savgol':
            if method=='savgol':
                liss=sig.savgol_filter(datas,2*delta+1,order,deriv=0)
                plt.plot(liss,'r')
                plt.legend (['signal','derivative','max','min','smoothing'])
            else:
                plt.legend (['signal','derivative','max','min'])
            plt.plot ([1,N],[0,0],'g--')

    return pmin, pmax    

# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    print("Auto-test if Python script launched from console")
    print("A noisy rectangular signal is displayed.")
    print("A smoothed version is displayed.")
    print("Derivative is displayed.")
    print("Min and max are indicated.")
    
    pvar=100; pmin=20; data=np.array([])
    for it in range(10):
         data=np.concatenate([data,np.ones(int(np.random.rand()*pvar)+pmin),
                    np.ones(int(np.random.rand()*pvar)+pmin)*-1])
    dataf=sig.lfilter([1,0],[1,-np.exp(-2*np.pi/30)],data)+np.random.randn(len(data))*0.1
    pmin,pmax = globalMinMax (dataf,enh='zak',graph=1)
    