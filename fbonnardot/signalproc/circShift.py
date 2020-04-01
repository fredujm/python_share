# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 13:44:24 2019

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

def circShift (datas,shift,forceft=False):
    """
    Circular shift of datas (use a Fourier Transform if shift is not an integer).

    Parameters
    ----------
    datas : vector or matrix(1 signal = 1 row for matrix) use np.array
        data to shift 
        
    shift : vector or float
        decal=datas [t-shift]
        
    forceft : bool, optional
        if True, force to use the Fourier Transform
        optional, False by default

    Return
    ------
    decal : vector or matrix (1 signal = 1 row for matrix)
        shifted datas
    
    Note
    ----
    The computing are faster if the number of samples are in the form of :math:`2^n` with n integer.

    Examples
    --------
    Example 1 :
        
    >>> import fbonnardot as fb; import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> a=np.concatenate((np.arange(65),np.arange(63,0,-1)))
    >>> line,=plt.plot (fb.circShift(a,0/10-6))
    >>> for d in range(1,129):
    >>>     line.set_ydata(fb.circShift(a,d/10-6))
    >>>     plt.pause(0.01)

    Example 2 :
        
    >>> import fbonnardot as fb; import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> a=np.concatenate((np.arange(65),np.arange(63,0,-1)))
    >>> a=np.array([a,a])
    >>> for b in range(1,101):
    >>>     fb.supPlot (fb.circShift(a,[b/10,-b/10]))
    >>>     plt.pause(0.01)
    >>>     plt.gca().clear()
    """
    
    # Creation              : Monday 8 April 2002      (MATLAB version)
    # Modifications         : Saturday 2 February 2019 (Translation to Python 3.6)
    #                         Thursday 6 February 2919 (Docstring in NumPy format and change forceft to bool)
    #                         Wednesday 1st April 2020 (Docstrings and auto-test)
    # Version               : 1.1 i

    # Check parameters
    if type(datas) is not np.ndarray:
        raise ValueError("datas should be numpy arrays")
    
    if datas.ndim==1:
        decal=circShift(np.array([datas]),shift,forceft)
        return decal[0]
    else:
         li,col=datas.shape
    
    if np.isscalar(shift):
        shift=np.ones(li)*shift
  
    if len(shift)!=li:
        raise ValueError("If shift is a vector it must have its size equal to signals numbers.")
     
    decal=np.zeros(datas.shape)
        
    # Pre computing for Fourier Transform
    halfcol=col//2
    if col & 1==0:
        # Even samples number
        # ex. 10 => f=[0 1 2 3 4 5 -4 -3 -2 -1]
        f=np.concatenate((np.arange(0,halfcol+1),np.arange(-halfcol+1,0)))/col
    else:
        # Odd samples number
        # ex.  9 => f=[0 1 2 3 4 -4 -3 -2 -1]
        f=np.concatenate((np.arange(0,halfcol+1),np.arange(-halfcol,0)))/col
    
    # Pour each signal (i.e. line)
    for index in range(li):
        sht=shift[index]
        # Two case :
        if sht==np.floor (sht) and forceft==False:
            # Integer shift
            # Replace a negative shift by a positive shift
            while sht<0:
                sht=sht+col
            # Set sht<col
            sht=int(sht % col)
            # Shift
            decal[index,sht:col]=datas[index,0:(col-sht)]
            decal[index,0:sht]  =datas[index,(col-sht):col]
        else:
            # Real shift => use Fourier Transform
            # Use FT [s (t-tau)]=TFT[s (t)].e^[-2.i.pi.f.tau]
            #   with phasis=e^[-2.i.pi.f.tau]
            # Compute FT
            tf=np.fft.fft (datas[index,:])
            # Compute phasis
            phase=np.exp(-2j*np.pi*f*sht)
            # Apply phase to FT
            tf=tf*phase
            # Compute inverse FT
            # If datas is real,
            if np.isreal(datas[index,0]):
                # decal should be real
                decal[index,:]=np.real(np.fft.ifft (tf))
            else:
                decal[index,:]=np.fft.ifft (tf)
    
    return decal

# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    print("Auto-test if Python script launched from console")
    print("You should see an animated figure with a moving triangle wave.")
    a=np.concatenate((np.arange(65),np.arange(63,0,-1)))
    line,=plt.plot (circShift(a,0/10-6))
    for d in range(1,129):
        line.set_ydata(circShift(a,d/10-6))
        plt.pause(0.01)
        