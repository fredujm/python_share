#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 21:10:43 2019

@author: Frédéric BONNARDOT, AGPL-3.0-or-later license
(c) Frédéric BONNARDOT, 2003-2020

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

import numpy             as np                 # matrix management
import scipy.signal      as sigp               # signal processing
import scipy.interpolate as interp             # interpolation
import matplotlib.pyplot as plt                # plot functions
import fbonnardot.detection.peakDetection as peakDetection
import fbonnardot.signalproc.circShift as circShift
import fbonnardot.display.periodPlot as periodPlot
import fbonnardot.display.supPlot as supPlot

def synchronisation2 (signal,period,method='maxCxyint',param=None,scaleopt='none',estsync=True,compens=False,graph=0):
    """
    Synchronisation of data by using intercorrelation or an amplitude based
    detection.
    
    Parameters
    ----------
    signal : vector
        signal to synchronize
    
    period : vector or int
        average period of the signal or vector with the reference signal
                  
    method : str, optional
        method used for synchronization
            * 'maxCxy'     - maximum of cross-correlation
            * 'baryCxy'    - barycenter of cross-correlation
            * 'maxCxyint'  - like Cxy but with 10x interpolation on Cxy for more precision
            * 'threshold'  - 1st sample at amplitude param
            * 'rthreshold' - 1st sample with positive slope and amplitude greater or equal to threshold
            * 'max'        - position of the maximum amplitude
            * 'ceps'       - robust cepstrum
            
        optionnal, 'maxCxyint' by default
                
    param : float tuple or None, optional
        According to method
            * 'threshold'  : float correspondinf to threshold
            * 'thresholdr' : tupple (threshold,min_slope) 
            * else not used (None)
        
        optional, None by default
    
    scaleopt : str, optional
        parameter for the correlation fonction
            * 'none'
            * 'biased'
            * 'unbiased'
            * 'circ' : correlation between reference and repetead 2 times signal
            
        optional, 'none' by default
                
    estsync : bool, optional
        True to fill synchr, False to return synchr=None
        
        optional, True by default
                
    compens : bool, optional
        True for compensation of slipping by shifting the begining of a bloc if
        the period change too much
        
        optional, False by default
                
    graph : int, optional
        Show results on one more graph
            * if graph & 1 = 1 -> supPlot
            * if graph & 2 = 2 -> block superposition before, after
            * if graph & 4 = 4 -> blocks
            
        optional, 0 by default
 
    Return
    ------
    synchr : Matrix Ncycles x period or None
        synchronized signals  
    
    delta : vector
        value of shift compared to period, ith value is at i*period-delta[i]
 
    Note
    ----
    Difference with synchronisation : this method correct the last period
    variation before each estimation.
    
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
    >>>
    >>> # Synchronisation
    >>> synchr,delta=fb.synchronisation2(signal,100,method='maxCxyint',param=1,scaleopt='unbiased',compens=True)
    >>>
    >>> # Graphs
    >>> pos=np.cumsum(100*np.ones(len(delta)))-100;pos=pos-delta;pos=np.array(pos,int);
    >>> plt.figure(); plt.plot(signal);pos=pos[0:-1];plt.plot(pos+50,signal[pos+50],'x')
    >>> plt.figure(); fb.supPlot(synchr,100)

    """
   
    # Creation      : Monday 1st December 2003 (MATLAB version)
    # Modifications : Thursday 31 January 2019 (Translation to Python 3.6)
    #                 Monday 4 February 2019 : Add graph
    #                 Thursday 7 February 2019 : Docstring in NumPy format
    #                                      and use bool for estsync and compens
    #                                      trigger method becomes threshold
    #                                      creates rthreshold (threshold + rising edge)
    #                                      suppress dec to have + or - shifts
    #                 Wednesday 27 February 2019 : circ option for correlation
    #                                              modulo period for graph=2
    #                 Wednesday 1st April 2020 (Auto-test)
    # Version       : 1.1 i


    # Check parameters

    if method not in ('maxCxy','baryCxy','maxCxyint','threshold','rthreshold','max','ceps'):
        raise ValueError('Illegal value for method.')
        
    if method in ('rthreshold','threshold') and param==None:
        raise ValueError('You should give a threshold in param for threshold and trigger methods')
        
    # Interpret period parameter   
    if not np.isscalar(period):
        reference=period
        period=len(reference)
    else:
        reference=signal[0:period]

    # Normalisation factor for correlation
    if scaleopt=='none':
        normCorr=1
    elif scaleopt=='biased':
        normCorr=period
    elif scaleopt=='unbiased':
        tau = np.arange(-(period - 1), period)
        normCorr=period-abs(tau)
    elif scaleopt=='circ':
        normCorr=1
    else:
        raise ValueError('Illegal value for scaleopt')
        
    # Estimation of shifts between each periods in the signal
    progressBar(0,"1/2")
    t=np.arange(period)   # signal[t] is compared to reference signal
    offset=0
    delta=[]              # List to store the estimated shifts
        
    while t[-1]<len(signal):
        # Compute correlation if necessary
        if method in ('maxCxy','baryCxy','maxCxyint'):
            if scaleopt=='circ':
                correlation=sigp.correlate(reference,np.tile(signal[t],2),'valid')
            else:
                # https://stackoverflow.com/questions/43652911/python-normalizing-1d-cross-correlation
                correlation=sigp.correlate(reference,signal[t],'full')/normCorr
            
          
        # Lag estimation
        if method=='maxCxy':
            posmax=np.argmax (correlation)
            delta.append(posmax-period+offset)
           
        elif method=='baryCxy':
            weight=np.abs(correlation)
            xi=np.arange(1,2*period)
            barycenter=np.round (np.sum(weight*xi)/np.sum(weight))
            delta.append(np.round(barycenter)-period+offset)
           
        elif method=='maxCxyint':
            interpol=interp.interp1d(np.arange(len(correlation)),correlation,'cubic')
            icorrelation=interpol(np.arange((len(correlation)-1)*10)/10)
            posmax=np.argmax(icorrelation)/10
            delta.append(posmax-period+offset)

        elif method=='threshold':
            #dec=min(period//2,t[0]) # To have + or - shifts use t-dec instead of t
            dec=0
            indice=np.where(signal[t-dec]>=param)[0]-dec
            if len(indice)!=0:
                delta.append(-indice[0]+offset)
            else:
                delta.append(0)
           
        elif method=='rthreshold':
            #dec=min(period//2,t[0]) # To have + or - shifts use t-dec instead of t
            dec=0
            indice=np.where(np.logical_and(signal[t-dec+2]-signal[t-dec]>param[1]/2,signal[t-dec+1]>=param[0]))[0]-dec
            if len(indice)!=0:
                delta.append(-indice[0]+offset)
            else:
                delta.append(0)
           
        elif method=='max':
            #dec=min(period//2,t[0]) # To have + or - shifts use t-dec instead of t
            dec=0 # no negative shifts
            indice=np.argmax (signal[t-dec])
            indice=indice-dec
            delta.append(-indice+offset)
           
        elif method=='ceps':
            prelev=np.concatenate((reference,signal[t],np.zeros(2*period)))
            # cepstre=np.real(np.fft.ifft(np.log(np.abs(np.fft(prelev)))))
            cepstre=np.real(np.fft.ifft(np.log(np.abs(np.fft.fft(sigp.correlate(prelev,prelev,'full')**2)))))
            cepstre=cepstre[0:(len(cepstre)//2)]
            cepstre[0:period//2+1]=0
            position,amp=peakDetection(cepstre,'diffInterp',10,10,10)
            position=np.array(position)
            sel=np.argmin(abs(position-period))
            position=position[sel]
            delta.append(position-1-period+offset)
       
        # Slip compensation
        if compens:
            compensation=delta[-1]-offset
            if abs(compensation)>1:
                compensation=int (compensation)
                t=t-compensation
                offset=offset+compensation
        else:
            compensation=0
    
        t=t+period
       
        progressBar(t[0]/len(signal),"1/2")
       
    progressBar(-1,'')
    delta=np.array(delta)

    # Signal shifting
    #delta=delta-delta[0]  
    if estsync:
        delta2=delta-delta[0]
        progressBar(0,"2/2")
        synchr=np.zeros((len(delta2),period))
        t=np.arange(period)
        for index in range(len(delta2)):
            if (t[-1]-int(delta2[index]))<len(signal):
                extrait=signal[t-int(delta2[index])]
                # decdec is the decimal part of shifting
                decdec=delta2[index]-int(delta2[index])
                if decdec!=0:
                    extrait=circShift (extrait,decdec)
                synchr[index,:]=extrait[0:period]
            t=t+period
            progressBar(index/len(delta2),"2/2")
        progressBar(-1,'')
    else:
        synchr=None
    
    if graph & 1==1:
        plt.figure()
        supPlot(synchr,scale='ind')
        plt.suptitle('Synchronisation : stack synchronised blocks')

    if graph & 2==2:
        plt.figure()
        plt.subplot(1,2,1)
        periodPlot(signal,period)
        plt.plot((-delta) % period,np.arange(len(delta))+1.5,'r.--')
        plt.title('Before')
        plt.subplot(1,2,2)
        supPlot(synchr,scale='ind')
        plt.title('After')
        plt.suptitle('Synchronisation : stack synchronised blocks')
        
    if graph & 4==4:
        plt.figure()
        colors=['r','b','k','c']
        N=len(signal)
        plt.plot(signal)
        ax=plt.gca()
        delta2=delta-delta[0]
        for index in range(len(delta2)):
            x1=index*period-delta2[index]
            x2=x1+period
            if x1>=0 and x1<N-period:
                y1=np.min(signal[int(x1):int(x2)])
                y2=np.max(signal[int(x1):int(x2)])
            else:
                y1=np.min(signal)
                y2=np.max(signal)
            ax.add_patch(plt.Rectangle((x1,y1),x2-x1,y2-y1,linewidth=1,edgecolor=colors[index % 4],facecolor='none'))
        plt.suptitle('Synchronisation : block position')

    return synchr,delta
    
def progressBar(position,step):
    """
    Display a text progress bar
    
    Parameters
    ----------
    
    position   : between 0 and 1
                 otherwise suppress the bar
    """
    
    if position>=0 and position<=1:
        nb_done=int(np.ceil(position*50))
        print("\rsynchro"+step+" : \u001b[44;1m"+">"*nb_done+"\u001b[0m\u001b[44m"+"-"*(50-nb_done)+"\u001b[0m",end='')
    else:
        print("\r"+" "*70+"\r\u001b[A")

# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    print("Auto-test if Python script launched from console")
    print("You should see a two figure.")
    print("Figure 1 : a noisy signal with peak. Peak are marked with a cross.")
    print("Figure 2 : a superposition of these peak. Peak are verticaly aligned.")

    # Generate test signal
    timp=np.array(np.cumsum(np.random.rand(30)*10+1000),int)-500
    signal=np.zeros(int(max(timp))+500)
    signal[timp]=3+np.random.randn(len(timp))*0.2
    signal=sigp.lfilter([1],[1,0.9],signal); signal+=np.random.randn(len(signal))*0.03
    #plt.figure(); plt.plot(signal)
    signal=sigp.decimate(signal,10)

    # Synchronisation
    synchr,delta=synchronisation2(signal,100,method='maxCxyint',param=1,scaleopt='unbiased',compens=True)

    # Graphs
    pos=np.cumsum(100*np.ones(len(delta)))-100;pos=pos-delta;pos=np.array(pos,int);
    plt.figure(); plt.plot(signal);pos=pos[0:-1];plt.plot(pos+50,signal[pos+50],'x')
    plt.figure(); supPlot(synchr,100)