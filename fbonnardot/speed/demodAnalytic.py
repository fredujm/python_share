#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 23:10:10 2019

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
import matplotlib.pyplot as plt          # plots
import matplotlib.widgets as wdg         # plots widgets

def demodAnalytic (signal,fdemod='interactive',method='diff'):
    """
    Retreive the phase and the frequency by using the analytic signal phase
    around a given frequency band.

    Parameters
    ----------
    signal : vector
        signal
        
    fdemod : str or vector, optional
        Can be a vector of 2 frequencies or a string :
            
            * String version:
                * 'interactive' : Display the Fourier Transform of r_signal and ask the user for the bands.
                * 'auto'        : Let the function choose the filter (can be only use for tacho signal and not working in all case !!!)
     
            * Vector version : a 2 elements vector containing the low and high normalized frequency for extracting the speed information.
                      
        Optional, 'interactive' by default.
              
    method  : str, optional
        Method for estimation of the instantaneous frequency :
            
            * 'diff'    :
                freq(n)=[phase(n+1)-phase(n)]/(2*pi) [unwrapping phase]
            
            * 'product' :
                freq(n)={angle [-sa(n+1).sa*(n-1)]+pi}/(4*pi) where sa is analytic signal
                
                equivalent to compute [phase (n+1)-phase (n-1)]/(4*pi) 
                
                (come from instfreq of Toolbox Temps Fréquence)
                
                approximation freq(1)=freq(2)
                  
        Optionnal, 'diff' by default

    Returns
    -------
    freq : vector
        instantaneous frequency
        
    phase : vector
        instantaneous phase
        
    fdemod : vector
        value of fdemod (useful if fdemod='auto' or 'interactive')

    Example
    -------
    
    >>> import fbonnardot as fb
    >>> import numpy as np; import matplotlib.pyplot as plt
    >>> t=np.arange(0,10,0.001)
    >>> phi=2*np.pi*(50*t+2*t**2); sig=np.sin(phi)
    >>> freq,phase,__=fb.demodAnalytic(sig)
    >>> plt.figure()
    >>> plt.subplot(2,1,1); plt.plot(t,sig)
    >>> plt.subplot(2,1,2); plt.plot(t,freq)

    Note
    ----
    Be careful of border effects.

    """

    # Creation              : Monday 16 July 2001      (MATLAB version)
    # Modifications         : Wednesday 2 January 2018 (Translation to Python 3.6)
    #                         Thursday 6 February 2019 (Docstring in NumPy format)
    #                         Wednesday 1st April 2020 (Auto-test)
    # Version               : 2.1 i

    # **************************************************************************
    # * Look at the parameters                                                 *
    # **************************************************************************
    
    l=len (signal)
    
    # Remove average to suppress DC peak
    signal=signal-np.mean (signal)
    
    # **************************************************************************
    # * Try to find a band for demodulation                                    *
    # **************************************************************************
    if np.size(fdemod)==1:
        tf=abs(np.fft.fft(signal))
        maxi=max(tf)
        mini=min(tf)
    
        #t=np.arange(len(tf))
        t2=np.arange(len(tf)//2)
        # -30 dB on smooth fft
        posi=np.argmax(np.abs(tf[t2]))
        maxi2=np.abs(tf[posi])
        seuil=maxi2/10**(30/20)
        lissage=100
        tfl=np.zeros(len(tf))
        tliss=np.arange(-lissage,lissage+1)
        for index in np.arange(lissage,len(tf)//2-lissage):
            tfl[index]=np.mean(np.abs(tf[index+tliss]))
        dem=np.where(tfl<seuil)[0]
        
        if len(dem)<2:
            fg=0
            fd=len(tf)//2-1
        else:
            fg=np.where((dem-posi)<0)[0]
            fd=np.where((dem-posi)>0)[0]
            fg=dem[fg[-1]]
            fd=dem[fd[0]]
            # Bigger band
            fen=fd-fg
            marge=0.25
            fg=np.floor(fg-fen*marge)/l
            fd=np.ceil (fd+fen*marge)/l
    
        if fdemod=='interactive':
            # interactive mode : ask the user for frequencies
            ff=plt.figure() 
            plt.plot(np.linspace(0,1,len(tf)),tf)
            plt.title("Draw a rectangle and clic on right button to validate")
            # plt.plot(np.linspace(0,1,len(tfl)),tfl)
            plt.xlabel ('Normalized Frequency')
            plt.ylabel ('Fourier transform')
            ax=plt.gca()
            ax.add_line(plt.Line2D([fg,fg],[mini,maxi],color='red',linestyle='--'))
            ax.add_line(plt.Line2D([fd,fd],[mini,maxi],color='red',linestyle='--'))
            ax.add_line(plt.Line2D([fd,fg],[mini,mini],color='red',linestyle='--'))
            ax.add_line(plt.Line2D([fd,fg],[maxi,maxi],color='red',linestyle='--'))

            def line_select_callback(eclick, erelease):
                if eclick.button==3:
                    rs.choiceok=1
 
            rs=wdg.RectangleSelector(ax,line_select_callback,drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
            
            rs.choiceok=0
            
            #rs.set_visible(True)
            #rs.extents= 1 , 5 , -0.5, 0.5 
            #rs.to_draw=True
            #rs.update()
            
            plt.show()
            
            while rs.choiceok==0:
                plt.pause(0.3)
                x1,x2,y1,y2 = rs.extents
                
            if x1<0:
                x1=0
                
            if x2>0.5:
                x2=0.5

            fg=x1
            fd=x2

            #a=input ('Low frequency (suggested: '+str(fg)+' - enter to use it) ? :')
            #if a!='':
            #    fg=a

            #a=input ('High frequency (suggested: '+str(fd)+' - enter to use it) ? :')
            #if a!='':
            #    fd=a
            plt.close(ff)
    
        fdemod=[fg,fd]
    
    fdemodl=np.round(np.array(fdemod)*l)
    
    # Filter + analytic signal
    tf=np.fft.fft(signal)
    tf[0:int(fdemodl[0])]=0
    tf[int(fdemodl[1]):]=0
    sa=np.fft.ifft(tf)
    
    # Demodulation
    if method=='diff':
        phi=np.unwrap(np.angle(sa))
        freq=np.diff(phi)/(2*np.pi)
    elif method=='product':
        phi=np.unwrap(np.angle(sa))
        n=np.arange(1,len(signal)-1)
        freq[n]=(np.angle(-sa[n+1]*np.conj(sa[n-1]))+np.pi)/4/np.pi
        freq[0]=freq[1]
    else:
        raise ValueError('Illegal value for method')
    
    phase=phi
    freq=np.append(freq,freq[-1])
    
    return freq,phase,fdemod

# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    print("Auto-test if Python script launched from console")
    print("You should see a graph with a two plateau.")
    print("Draw a rectangle on the left one and right click.")
    print("Another graph with a ramp should appear.")
    t=np.arange(0,10,0.001)
    phi=2*np.pi*(50*t+2*t**2); sig=np.sin(phi)
    freq,phase,__=demodAnalytic(sig)
    plt.figure();
    plt.subplot(2,1,1); plt.plot(t,sig)
    plt.subplot(2,1,2); plt.plot(t,freq)
    