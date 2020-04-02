#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 22:33:24 2019

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

def syncAv (datas,blocSize,resid=False):
    """
    Computes the synchronous average of one or more signals.
    
    Parameters
    ----------
    datas : np.array vector or matrix (nb_sig x sig_len) 1 signal=1 row
        signals used for compute synchronous average 
        
    blocSize : int or float
        size of a block to make the mean (not necessary an integer)
        
    resid : boolean, optional
        returns the residual if resid is True
        optional, False by default

    Returns
    -------
    sav : np.array
        Synchronous average of each signals
        
    nbBlocs : int
        Number of blocs used for estimating the synchronous average
        if this size is not integer, the data will be interpolated to make this size integer

    residual : np.array, optional
        residual returned only if resid is True

    Note
    ----
    * A warning is made if the number of row is greater than the number of column.
    * A warning is made if there is not an integer number of cycles
    
    Examples
    --------
    
    Case were period is an integer
    
    >>> import fbonnardot as fb
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>>
    >>> period=128; cycles=100
    >>> zz=np.zeros((period-1)//2)
    >>> exitation=np.tile(np.concatenate([zz,[0,1],zz]),[cycles])
    >>> sig=signal.lfilter([1],[1,0.3,-0.2,0.4,0.6],exitation)
    >>> sig=sig+np.random.randn(period*cycles)*0.1
    >>>
    >>> sav,nbBlocs=fb.syncAv (sig,period)
    >>> plt.figure()
    >>> plt.plot(sig.T,'b')
    >>> plt.plot(sav.T,'r')
    >>> plt.legend(['signal (1 period)','synchronous average'])
    >>> plt.xlim([0,period])
    
    Case with an real period
        
    >>> import fbonnardot as fb
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np    
    >>>
    >>> period=127.4; cycles=100
    >>> sig=np.sin(2*np.pi*np.arange(int(period*cycles))/period)
    >>> sig=sig+np.random.randn(np.size(sig))*0.1
    >>>
    >>> sav,nbBlocs=fb.syncAv (sig,period)
    >>> plt.figure()
    >>> plt.plot(sig,'b')
    >>> plt.plot(np.linspace(0,period,int(np.ceil(period))),sav,'r')
    >>> plt.legend(['signal (1 period)','synchronous average'])
    >>> plt.xlim([0,period])

    """

    # Creation              : Thursay 23 August 2001 (MATLAB version)
    # Modifications         : Monday 7 January 2019  (Translation to Python 3.6)
    #                         Saturday 9 March 2019   (Can return the residual)
    #                         Thursday 2 April 2020 (Auto test)
    # Version               : 1.4 i

    # Original name : msynchrone.m

    if np.ndim(datas)>1:
        li,col=np.shape (datas)
    else:
        col=np.size(datas)
        li=1
        
    if blocSize>col:
        raise ValueError ('The datas must have at least 1 blocs.')
    
    if blocSize<=0:
        raise ValueError ('Bloc must be strictly positive.')
    
    if li>=col:
        warnings.warn('Number of row>number of column ? 1 row = 1 signal')
   
    # Manage not integer periods
    if type(blocSize) is not int:
        warnings.warn ('Not an integer period => resampling.')
        step=blocSize/np.ceil(blocSize)
        if li>1:
            donnees2=np.zeros(li,int(np.ceil((col-1)/step)))
            for index in range(li):
                ifunc=interp.interp1d(np.arange(1,col+1),datas[index,:],kind='cubic')
                donnees2[index,:]=ifunc(np.arange(1,col,step))
        else:
            ifunc=interp.interp1d(np.arange(1,col+1),datas,kind='cubic')
            donnees2=ifunc(np.arange(1,col,step))
        if resid:
            sav,nbBlocs,res=syncAv (donnees2,int(np.ceil(blocSize)),resid)
            residu=res
        else:
            sav,nbBlocs=syncAv (donnees2,int(np.ceil(blocSize)),resid)
    else:
        # Compute synchronous average
        nbBlocs=col//blocSize
        
        if col % blocSize!=0:
            warnings.warn ('The signal don\'t contain an integer number of intergers, it will be truncated.')
        
        if nbBlocs==1:
            warnings.warn ('With only 1 bloc it is not synchronous average !!!')
        
        if li>1:
            # nbr sig x sig_len -> nbr_sig x nbBlocs x blocSize
            tens=np.reshape(datas[:,0:(nbBlocs*blocSize)],[li,nbBlocs,blocSize])
            # nbr_sig x nbBlocs x blocSize -> nbr_sig x blocSize
            sav=np.mean(tens,1)
            residu=datas-np.tile(sav,nbBlocs+1)[0:li,0:col]
        else:
            # sig_len -> nbBlocs x blocSize
            tens=np.reshape(datas[0:(nbBlocs*blocSize)],[nbBlocs,blocSize])
            sav=np.mean(tens,0)
            residu=datas-np.tile(sav,nbBlocs+1)[0:col]
            
    if resid:
        return sav,nbBlocs,residu
    else:
        return sav,nbBlocs

# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    print("Auto-test if Python script launched from console")
    print("Figure 1 shows in blue the first period of an impulsive noisy signal.")
    print("   Its synchronous average is in red.")
    print("Figure 2 shows in blue the first period of an sine noisy signal.")
    print("   Its synchronous average is in red.")
    
    from scipy import signal
    import matplotlib.pyplot as plt

    period=128; cycles=100
    zz=np.zeros((period-1)//2)
    exitation=np.tile(np.concatenate([zz,[0,1],zz]),[cycles])
    sig=signal.lfilter([1],[1,0.3,-0.2,0.4,0.6],exitation)
    sig=sig+np.random.randn(period*cycles)*0.1

    sav,nbBlocs=syncAv (sig,period)
    plt.figure()
    plt.plot(sig.T,'b')
    plt.plot(sav.T,'r')
    plt.legend(['signal (1 period)','synchronous average'])
    plt.xlim([0,period])
    
    # Case with an real period
    
    period=127.4; cycles=100
    sig=np.sin(2*np.pi*np.arange(int(period*cycles))/period)
    sig=sig+np.random.randn(np.size(sig))*0.1

    sav,nbBlocs=syncAv (sig,period)
    plt.figure()
    plt.plot(sig,'b')
    plt.plot(np.linspace(0,period,int(np.ceil(period))),sav,'r')
    plt.legend(['signal (1 period)','synchronous average'])
    plt.xlim([0,period])
