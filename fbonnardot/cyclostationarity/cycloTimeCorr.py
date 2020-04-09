# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 17:15:04 2019

@author: Frédéric BONNARDOT, AGPL-3.0-or-later license
(c) Frédéric BONNARDOT, 2017-2019

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
import matplotlib.pyplot as plt          # plots
from mpl_toolkits.mplot3d import axes3d  # 3D projection
import fbonnardot.cyclostationarity.syncAv

def cycloTimeCorr (x,y,period,vect_tau,graph=0):
    """
    Compute temporal (inter)-correlation of a cyclostationnary signal.

    Parameters
    ----------   
    x,y : vector,
        signals x and y must have the same size
        
    period : scalar,
        cyclic period of the signal to consider
        
    vect_tau : vector,
        delays (lag) for computing (even integers)

    graph : scalar, optionnal
        display a graph if 1
        optionnal, 0 by default
        
    Returns
    -------
    Rxy : matrix of size period x len(vect_tau)
        Estimated correlation Rxy(t,tau)
                      
    Note
    -----
    * To estimate correlation, we compute
        syncAv(x(t-tau/2)*conj(y(t+tau/2)),period)

    * Since synchronous average is used, all cyclic period not multiple of period
        are destroyed or reduced

    Example
    -------
    >>> import fbonnardot as fb
    >>> import scipy.signal as signal; import numpy as np
    >>> per=12; N=130*per
    >>> bruit=np.random.rand(N)-0.5
    >>> bruit=signal.lfilter([1,0.9,0.8,0.7,0.4,0.5,0.2,0.1],1,bruit) # Correlate noise
    >>> data=np.sin(2*np.pi/per*np.arange(N))*bruit
    >>> tau=np.arange(0,20,2)
    >>> Rxx=fb.cycloTimeCorr(data,data,per,tau,graph=1)
    """
    
    # Creation              : Tuesday 4 July 2017      (MATLAB version)
    # Modifications         : Tuesday 19 November 2019 (Translation to Python 3.7)
    #                         Thursday 2 April 2020    (Docstring anf Auto test)
    #                         Thurday 9 April 2020 (change name form cyclicTimeCorr to cycloTimeCorr)
    # Version               : 1.1 i

    Nx=len(x)
    Ntau=len(vect_tau)

    if Nx!=len(y):
        raise ValueError ("x and y must have the same size")

    Rxy=np.zeros((period,Ntau))


    for index in range(Ntau):
        progressBar(index/Ntau)
        tau=vect_tau[index]
        
        t=np.arange(tau//2+1,Nx-tau//2)
        t=t[0:int(np.floor(len(t)/period))*period] # integer number of period
        sAv,nb=fbonnardot.cyclostationarity.syncAv(x[t-tau//2]*np.conj(y[t+tau//2]),period)
        Rxy[:,index]=sAv

    progressBar(-1)
    
    # Graph if graph=1
    if graph==1:
        fig = plt.figure()
        t=np.arange(0,period)
        ax = fig.add_subplot(111, projection='3d')
        for index in range(Ntau):
            ax.plot(vect_tau[index]*np.ones(len(t)),t,np.abs(Rxy[:,index]))
        ax.set_xlabel(r'$\tau$'); ax.set_ylabel(r'$t$'); ax.set_zlabel(r'$|Rxy(t,\tau)|$');
        ax.view_init(elev=30, azim=60)
        plt.title('Modulus of Time Correlation')
        plt.show()
    
    return Rxy


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
        print("\rcycloTimeCorr : \u001b[44;1m"+">"*nb_done+"\u001b[0m\u001b[44m"+"-"*(50-nb_done)+"\u001b[0m",end='')
    else:
        print("\r"+" "*70+"\r\u001b[A")
        
# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    print("Auto-test if Python script launched from console")
    print("A 3D figure is displayed.")
    print("At lag tau=0 there is 2 large peaks.")
    print("The amplitude of these peaks vanished as tau increase.")
    
    import scipy.signal as signal
    per=12; N=130*per
    bruit=np.random.rand(N)-0.5
    bruit=signal.lfilter([1,0.9,0.8,0.7,0.4,0.5,0.2,0.1],1,bruit) # Correlate noise
    data=np.sin(2*np.pi/per*np.arange(N))*bruit
    tau=np.arange(0,20,2)
    Rxx=cycloTimeCorr(data,data,per,tau,graph=1)
