#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:03:21 2019

@author: Frédéric BONNARDOT, CC BY-NC-SA 4.0 license

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/

This code is given as is without warranty of any kind.
In no event shall the authors or copyright holder be liable for any claim
                                                   damages or other liability.

If you change or adapt this function, change its name (for example add your
                                                       initial after the name)
"""

import matplotlib.pyplot as plt          # plot
import matplotlib        as mpl
import numpy             as np           # manage vectors

def verticalLabel (x,text,color='b',linestyle='-',linewidth=0.5,position='top',fontsize=10,orient='vert',ax=None):
    """
    Put vertical labeled lines on the figure.

    Parameters
    ----------
    x : scalar or vector for more marks
        abcissa
        
    text : string
        text to display (use %i for display mark number (start at 1))
        
    color : string, optional
        color
        optional 'b' by default
        
    linestyle : string, optional
        style '-' or '--' or '-.' or ':' or 'None' ...
        optional '-' by default
        
    linewidth : float, optional
        width
        optional 0.5 by default
        
    position : string, optional
        'top' or 'bottom'
        optional, 'top' by default
        
    fontsize : float, optional
        font size, optional, 10 by default
        
    orient : string, optional
        'vert' or 'horiz'
        vert by default
        
    ax : Axes, optional
        The axes to draw to (None means current axis given by plt.gca())
        optional, None by defaut

    Return
    ------
    h : list
        list of lines added

    Example
    -------
    >>> import fbonnardot as fb; import numpy as np; import matplotlib.pyplot as plt
    >>> plt.figure()
    >>> Ts=0.1; freq=0.3
    >>> tps=np.arange(0,5,Ts); signal=np.sin(2*np.pi*tps*freq)
    >>> plt.plot(tps,signal)
    >>> fb.verticalLabel(1/freq,'period','r','--',1,'top')
    >>> fb.verticalLabel(0.5/freq,'1/2 period',[0.4,0.4,0],'-',3,'bottom',13)
    >>> fb.verticalLabel(np.arange(1,5),'{:d} sec',[0.5,0.5,0.95],'--',0.5,'top',10,'horiz')
    """

    # Creation              : Monday 12 December 2017 (MATLAB version)
    # Modifications         : Tuesday 12 March 2019   (Python translation)
    #                         Tuesday 31 March 2020 (NumPy docstring - autotest)
    # Version               : 1.1 i
    
    # For drawing in Python :
    # http://www.python-simple.com/python-matplotlib/dessin-matplotlib.php
    
    if ax==None:
        ax=plt.gca()
        
    if np.isscalar(x):
        x=[x]
        
    YLim=ax.get_ylim()
    h=[]
    for index in range(len(x)):
        h.append(ax.add_artist(mpl.lines.Line2D((x[index],x[index]),YLim, color = color,linestyle=linestyle,linewidth=linewidth)))
        #% Ins�re la ligne sous les autres �l�ments
        #chH = get(gca,'Children');
        #set(gca,'Children',[chH(2:end);chH(1)]);
        if position=='top':
            if orient=='vert':
                h.append(ax.add_artist(mpl.text.Text(x[index],YLim[1],text.format(index+1),color=color,horizontalalignment='right',verticalalignment='top',rotation=90,fontsize=fontsize)))
            else:
                h.append(ax.add_artist(mpl.text.Text(x[index],YLim[1],text.format(index+1),color=color,horizontalalignment='center',verticalalignment='top',rotation=0,fontsize=fontsize)))
        else:
            if orient=='vert':
                h.append(ax.add_artist(mpl.text.Text(x[index],YLim[0],text.format(index+1),color=color,horizontalalignment='right',verticalalignment='bottom',rotation=90,fontsize=fontsize)))
            else:
                h.append(ax.add_artist(mpl.text.Text(x[index],YLim[0],text.format(index+1),color=color,horizontalalignment='center',verticalalignment='bottom',rotation=0,fontsize=fontsize)))
 
    return h
 
# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    print("Auto-test if Python script launched from console")
    print("You should see a graph with a sine wave, vertical labels each second, at period and half period.")
    plt.figure()
    Ts=0.1; freq=0.3
    tps=np.arange(0,5,Ts); signal=np.sin(2*np.pi*tps*freq)
    plt.plot(tps,signal)
    verticalLabel(1/freq,'period','r','--',1,'top')
    verticalLabel(0.5/freq,'1/2 period',[0.4,0.4,0],'-',3,'bottom',13)
    verticalLabel(np.arange(1,5),'{:d} sec',[0.5,0.5,0.95],'--',0.5,'top',10,'horiz')   
    