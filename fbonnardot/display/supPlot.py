#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 14:02:10 2018

@author: Frédéric BONNARDOT, CC BY-NC-SA 4.0 license

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/

This code is given as is without warranty of any kind.
In no event shall the authors or copyright holder be liable for any claim
                                                   damages or other liability.

If you change or adapt this function, change its name (for example add your
                                                       initial after the name)
"""


import math                              # for math.inf
import numpy as np                       # matrix management
import warnings
import matplotlib.pyplot as plt          # Plot
import matplotlib.backend_tools as tools # To create custom toolbar

plt.rcParams['toolbar'] = 'toolmanager'  # Pour ajouter une toolbar

def supPlot(datas,N=math.inf,offset=0,Ts=1,names=None,orient='vert',overlap=0,scale='ind',axes=None,t_axis=-1,sig_axis=None,fmt=None):
    """
    Display a set of signal by overlapping them
    
    Parameters
    ----------
    
    datas : matrix or tensor (np.array)
        datas to plot 
          - (matrix) nb_signal x time
          - or 3D array for many signal per stacks realization x nb_signal x time
          
    N : integer, optionnal
        last sample to plot (1 means 1st sample) must be > 1
        optional, math.inf by default (i.e. plot all samples)
        
    offset : scalar or vector, optionnal
        offset
        according to its sign offset is interpreted differently
            - offset > 0 : Display the data beginning at the offset+1 sample
            - offset < 0 : Tells the sample number corresponding to abscissa 0
                in the x axis
            - if offset is a vector, it will be like
                [display sample0] (with no sign interpretation)
        optional, 0 by default
        
    Ts : scalar of vector, optionnal
        - Sampling period or time vector
        - or vector corresponding to the abscissas
        optional, 1 by default
        
    names : array of string, optionnal
        names of the datas
        the name of the signals is displayed on the left
        ex. : ['channel A','channel B']
        if there is more the 20 signals, some name will not be displayed
        optional, None by default
        
    orient : string, optionnal
        Orientation of the signals name
            - 'horiz' : horizontal
            - 'vert'  : vertical
            - 'no'    : no signal name displayed
        optionnal, 'vert' by default
        
    overlap : integer, optionnal
        - Overlapping factor between signals between 0 and 0.999
        - or -1  to superpose the signals
        optionnal, 0 by default
        
    scale : string, optionnal
        Scale of signals
            - 'ind' : each signal have its own scale to fit in the n, n+1 box
            - 'glo' : same scale for each signal
        optionnal, 'ind' by default
        
    axes : object, optionnal
        Axes to draw the datas or None to use current Axes
        optionnal, None by default
        
    t_axis : vector, optionnal
        Axis associated to time,
        optionnal, -1 by default
        
    sig_axis : integer, optionnal
        Axis associated with a signal (i.e. stacks)
        optional, None by default
        None means other dimension for matrixes or -2 for 3D arrays
        
    fmt : string or list of string, optionnal
        format for plotting curves (e.g. 'b-')
            - str if datas is a matrix
            - or list of str if datas is 3D array, optional
        None by default
               
    Returns
    -------
    M         :number of signals
    
    Notes
    -----
    - the ith signal is between i and i+1 (1st signal i=1)
    - if overlap<>0, the min, max, the grid aren't displayed.
    - in case of 3D array, averaging against first axis for welch like Fourier
    
    Examples
    --------
    
    >>> import fbonnardot as fb; import numpy as np
    
    >>> datas=np.array([[1.,0.,0.,-1.,0.,1.],[2.,1.,0.,2.,0.,3.],[0.,0.,1.,-1.,1.,0.]])
    >>> fb.supPlot(datas,Ts=0.1,names=['sig 1','sig 2','sig 3'])

    >>> datas=np.array([[1.,0.,0.,-1.,0.,1.],[2.,1.,0.,2.,0.,3.],[0.,0.,1.,-1.,1.,0.]])
    >>> datasn=np.tile(datas,(4,1,1))+np.random.randn(4,3,6)
    >>> fb.supPlot(datasn,Ts=0.1,names=['sig 1','sig 2','sig 3'])
    
    In order to test FFT in the Toolbar:
    >>> t=np.arange(0,0.05,0.001)
    >>> datas=np.array([np.cos(2*3.14*50*t),np.cos(2*3.14*150*t),np.cos(2*3.14*200*t)])
    >>> fb.supPlot(datas,Ts=0.001,names=['50 Hz','150 Hz','200 Hz'])
    
"""    

    # Creation              : Thursay 12 July 2001      (MATLAB version)
    # Modifications         : Sunday 23 December 2018 (Translation to Python 3.6)
    #                         Monday 9 December 2019 (Add axes parameter)
    #                         Thurday 26 December 2019 (Can use 3D Matrixes)
    #                         Thursday 6 February 2020 (orient='no' option)
    #                         Tuesday 31 March 2020 (NumPy docstring - autotest)
    # Version               : 1.92 i


    # Find position of samples and signal axis in matrix datas
    mat_index=np.arange(datas.ndim)
    p_samples=mat_index[t_axis]
    if sig_axis==None:
        if datas.ndim==2:
            p_sig=1-p_samples
        else:
            p_sig=-2
    else:
        p_sig=mat_index[sig_axis]
    
    nb_sig=datas.shape[p_sig]
    t_sig=datas.shape[p_samples]
    #[nb_sig,t_sig]=datas.shape

    # Check that p_sig if different of t_sig
    if p_sig==p_samples:
        raise ValueError('Parameter t_axis should be different of sig_axis')
    
    # Check that signal length greater than number of signal
    if nb_sig>t_sig:
        warnings.warn('Number of signals to display greater than their length.\nYou may have forgot to transpose datas parameter, press Ctrl-C to stop.')
        
    # Get current axes if axes is None
    if axes==None:
        axes=plt.gca()
        menu=True
    else:
        menu=False
        
    # Manage optional parameters ...
    # ... Parameter N
    if N==math.inf:
        N=t_sig
    elif  N>t_sig:
        raise ValueError('Parameter N cannot be greater than signal length.')
    elif N<2:
        raise ValueError('Parameter N cannot be lower than 2.')
    
    if type(N) is not int:
        raise ValueError('N should be an integer.')
    
    # ... Parameter offset
    if np.isscalar(offset) and type(offset) is not int:
        raise ValueError('offset should be an integer.')
    
    if np.isscalar(offset):
        if offset>=N-1:
            raise ValueError('offset cannot be greater than N-2')
        elif offset>=0:
            firstSample=offset
            initialAbscissa=0
        else:
            firstSample=0
            initialAbscissa=-offset-1
    elif len(offset)==2:
        firstSample=offset[0]
        initialAbscissa=offset [1]-1
    else:
        raise ValueError('Offset can\'t have more than 2 elements.')
    
    # ... Ts
    if not np.isscalar(Ts):
        if (len(Ts) != t_sig):
            raise ValueError('Ts must have the same size than each signals.')
    
    # ... noms
    if names!=None:
        if len(names)!=nb_sig:
            raise ValueError ('The last signals don\'t have names.')
                              
    # ... orientation
    if orient!='vert' and orient!='horiz' and orient!='no':
        raise ValueError('Bad value for orientation.')
    
    # ... overlap
    if (abs(overlap)>=1 or abs(overlap)<0) and overlap!=-1:
        raise ValueError('Overlap must be in [0;1[.')
    
    # ... scale
    if scale=='glo':
        sameScale=1
    elif scale=='ind':
        sameScale=0
    else:
        raise ValueError('Bad value for scale.')
    
    if overlap==-1:
        sameScale=1
    
    #...fmt
    if fmt==None:
        fmt='b'
        
    if datas.ndim==3 and np.ndim(fmt)==0:
        fmt=np.tile(fmt,datas.shape[0])
    
    # Extract data to display (work on a copy of datas)
    temp=np.array(datas)
    temp=np.swapaxes(temp,p_samples,0)
    if p_sig==0:
        p_sig=p_samples
    if datas.ndim==3:
        temp=np.swapaxes(temp,p_sig,1)
    # Now temp size is nb_samples x nb_sig x nb_realizations
    datas2=np.array(temp.T)
    temp=temp[firstSample:N,:]
    # if p_sig==0:
    #     temp=np.array(datas[:,firstSample:N].T)
    # else:
    #     temp=np.array(datas[firstSample:N,:])
        
    # Signal normalisation : they should be in index*(1-overlap)+[-0.5;0.5]
    if datas.ndim==2:
        maximum=np.max (temp,0)
        minimum=np.min (temp,0)
    else:
        maximum=np.max (temp,(0,2))
        minimum=np.min (temp,(0,2))
                
    if sameScale==1:
        minimum[:]=np.min(minimum)
        maximum[:]=np.max(maximum)
    
    if overlap!=-1:
        for index in range(nb_sig):
            if maximum[index]==minimum[index]:
                warnings.warn('The signal n°'+str(index)+' is constant !!!')
                temp[:,index]=(index+1)*(1-overlap)+0.5
            else:
                temp[:,index]=(index+1)*(1-overlap)+0.5+(temp[:,index]-(maximum[index]+minimum[index])/2)/(maximum[index]-minimum[index])
    
    # Create or extract time vector
    if np.isscalar(Ts):
        t=np.arange((firstSample-initialAbscissa),(N-initialAbscissa))*Ts
    else:
        t=Ts[firstSample:N]
        
    # Plots the data
    if datas.ndim==2:
        axes.plot(t,temp,fmt)
    else:
        for index in range(temp.shape[-1]):
            axes.plot(t,temp[:,:,index],fmt[index])

    # Choose area to display
    axes.set_xlim(t[0],t[-1])
    if overlap!=-1:   
        axes.set_ylim(1-overlap,nb_sig*(1-overlap)+1)
    else:
        axes.set_ylim(min(temp),max(temp))
        names=None
    
    
    # Display a grid if no overlap
    if overlap==0:
        # Limit number of grid line if more than 20 signals
        if nb_sig>20:
            pastick=math.ceil (nb_sig/20)
        else:
            pastick=1
        axes.set_yticks(np.arange(2,nb_sig+1,pastick),[])
        axes.grid()
    
    # Display names
    if names!=None:
        #set (handle,'YTickLabel',[]);
        # Limit the number of name to display if more than 20 signals
        if nb_sig>20:
            namestep=math.ceil (nb_sig/20)
        else:
            namestep=1
        
        for index in np.arange(0,nb_sig,namestep):
            name=names[index]
            if orient=='vert':
                axes.text(t[0],(index+1)*(1-overlap)+0.5,name,rotation=90,ha='right',va='center')
            elif orient=='horiz':
                axes.text(t[0],(index+1)*(1-overlap)+0.5,name,ha='right',va='center')
    
    # Display minimum and maximum values if no overlap
    if overlap==0 and sameScale==0 and nb_sig<20:
        if datas.ndim==2:
            for index in range(nb_sig):
                text="{:01.2e}".format(np.min(datas[index,firstSample:N]))
                axes.text(t[-1],index+1,text,ha='left',va='bottom')
                text="{:01.2e}".format(np.max(datas[index,firstSample:N]))
                axes.text(t[-1],index+2,text,ha='left',va='top')
        else:
            for index in range(nb_sig):
                text="{:01.2e}".format(np.min(datas[:,index,firstSample:N]))
                axes.text(t[-1],index+1,text,ha='left',va='bottom')
                text="{:01.2e}".format(np.max(datas[:,index,firstSample:N]))
                axes.text(t[-1],index+2,text,ha='left',va='top')  


    # Classes associated to the toolbar

    class StretchTool(tools.ToolBase):
        """Switch between global and individual scale"""
        default_keymap = 'S'
        description = 'Stretch individualy each signal or apply the same global scale'
        # image = None
        name = 'Stretch'
    
        def __init__(self, *args, effect, **kwargs):
            self.name=effect
            super().__init__(*args, **kwargs)
    
        def trigger(self, *args, **kwargs):
            spparams=self.figure.spparams
            plt.figure()
            if spparams['scale']=='glo':
                scale='ind'
            else:
                scale='glo'
            supPlot(spparams['datas'],spparams['N'],spparams['offset'],spparams['Ts'],spparams['names'],spparams['orient'],spparams['overlap'],scale,fmt=fmt)

    class FourierTool(tools.ToolBase):
        """Display Fourier Transform modulus (Hamming Window)"""
        default_keymap = 'F'
        description = 'Display the Fourier Transform modulus of the signals (Hamming Window)'
        # image = None
        name = 'FFT'
      
        def __init__(self, *args,unit, **kwargs):
            self.name='FFT('+unit+')'
            self.unit=unit
            super().__init__(*args, **kwargs)

        def trigger(self, *args, **kwargs):
            spparams=self.figure.spparams
            # Compute Fourier Transform of each data
            datas=spparams['datas']            
            [nb_sig,t_sig]=datas.shape[-2:]
            datasft=np.zeros([nb_sig,t_sig])
            window=np.hamming(t_sig)
            for index in range(nb_sig):
                if datas.ndim==2:
                    datasft[index,:]=np.abs(np.fft.fft(datas[index,:]*window))
                else:
                    datasft[index,:]=np.mean(np.abs(np.fft.fft(datas[:,index,:]*window,axis=1)),axis=0)
            if self.unit=='dB':
                datasft=20*np.log10(datasft)
            plt.figure()
            supPlot(datasft,math.inf,0,1/spparams['Ts']/t_sig,spparams['names'],spparams['orient'],spparams['overlap'],spparams['scale'])


    class CepstrumTool(tools.ToolBase):
        """Display Real Cepstrum"""
        default_keymap = 'C'
        description = 'Display the Real Cepstrum of the signals'
        # image = None
        name = 'Cepstrum'

        def trigger(self, *args, **kwargs):
            spparams=self.figure.spparams
            # Compute Fourier Transform of each data
            datas=spparams['datas']            
            [nb_sig,t_sig]=datas.shape[-2:]
            datasrceps=np.zeros([nb_sig,t_sig])
            for index in range(nb_sig):
                if datas.ndim==2:
                    datasrceps[index,:]=np.real(np.fft.ifft(np.log(np.abs(np.fft.fft(datas[index,:])))))
                else:
                    datasrceps[index,:]=np.real(np.fft.ifft(np.log(np.mean(np.abs(np.fft.fft(datas[:,index,:],axis=1)),axis=0))))
            plt.figure()
            supPlot(datasrceps,math.inf,0,spparams['Ts'],spparams['names'],spparams['orient'],spparams['overlap'],spparams['scale'])


    class OverlapTool(tools.ToolBase):
        """Overlap all signals"""
        default_keymap = 'O'
        description = 'Overlap all signals'
        # image = None
        name = 'Overlap'

        def trigger(self, *args, **kwargs):
            spparams=self.figure.spparams
            datas=spparams['datas']
            [nb_sig,t_sig]=datas.shape[-2:]
            t=np.arange(t_sig)/spparams['Ts']
            plt.figure()
            if datas.ndim==2:
                plt.plot(t,datas.T)
            else:
                for index in range(datas.shape[0]):
                    plt.plot(t,datas[index].T)

    # User menu (if no axes is given)
    if menu==True:
        # Store the params in the figure
        spparams={"datas":datas2,"N":N,"offset":offset,"Ts":Ts,"names":names,"orient":orient,"overlap":overlap,"scale":scale,"fmt":fmt}
        fig=plt.gcf()
        fig.spparams=spparams
    
        # Set up the toolbar
        if scale=='glo':
            effect='Stretch'
        else:
            effect='UnStretch'
        fig.canvas.manager.toolmanager.add_tool(effect, StretchTool,effect=effect)
        fig.canvas.manager.toolmanager.add_tool('Overlap', OverlapTool)
        fig.canvas.manager.toolmanager.add_tool('FFT(lin)', FourierTool,unit='lin')
        fig.canvas.manager.toolmanager.add_tool('FFT(dB)', FourierTool,unit='dB')
        fig.canvas.manager.toolmanager.add_tool('Cepstrum', CepstrumTool)
            
        fig.canvas.manager.toolbar.add_tool(effect,    'supplot', 0)
        fig.canvas.manager.toolbar.add_tool('Overlap', 'supplot', -1)
        fig.canvas.manager.toolbar.add_tool('FFT(lin)','supplot', -1)
        fig.canvas.manager.toolbar.add_tool('FFT(dB)', 'supplot', -1)
        fig.canvas.manager.toolbar.add_tool('Cepstrum','supplot', -1)
    
    # Missing in comparison with Matlab version :
    #    psd lin and log with block size of 256/512/1024/2084/4096
    #    timefrequency
    #    extract a signal
    #    remove a signal
    #    overlap ((0:19)*5 %)
 
    return nb_sig

# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    print("Auto-test if Python script launched from console")
    print("You should see a dialog box to adjust options, and a graph.")
    datas=np.array([[1.,0.,0.,-1.,0.,1.],[2.,1.,0.,2.,0.,3.],[0.,0.,1.,-1.,1.,0.]])
    supPlot(datas,Ts=0.1,names=['sig 1','sig 2','sig 3'])
    