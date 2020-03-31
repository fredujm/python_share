# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 09:14:48 2019

@author: Frédéric BONNARDOT, CC BY-NC-SA 4.0 license

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/

This code is given as is without warranty of any kind.
In no event shall the authors or copyright holder be liable for any claim
                                                   damages or other liability.

If you change or adapt this function, change its name (for example add your
                                                       initial after the name)
"""

import sys # Requis pour PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg, NavigationToolbar2QT)

import numpy as np

class plotMatrix(QtWidgets.QMainWindow):
    """
    Draw an picture associated to a matrix and provide a toolbox to adjust visualisation.

    Example
    -------
    >>> import fbonnardot as fb; import numpy as np
    >>> data=np.array([[0,0,0,1,0],[1,2,1,0,0],[2,0,4,0,0],[3,0,0,6,0]])
    >>> fb.plotMatrix(data,0.1,2,'x','y','z')
    
    Warning
    -------
    Save your data before using this program : it can freeze Python
    """
    # Creation :    : Saturday 27 July 2019
    # Modifications : Monday 9 September 2019 (Use Qt instead of Tcl/Tk)
    #               : Tuesday 31 March 2020 (NumPy docstring - autotest update)
    # Version       : 1.2 i
    def __init__(self, data, stepx=1, stepy=1,xlabel='',ylabel='',zlabel=''):
        """
        Create the image properties window
        
        Parameters
        ----------
        
        data : matrix
            data to plot (y x x)
        
        stepx : integer, optional
            step between each elements on x axis
        
        stepy : integer, optional
            step between each elements on y axis
        
        xlabel : string, optional
            label for x axis
        
        ylabel : string, optional
            label for y axis
        
        zlabel : string, optional
            label for z axis
            
        Return
        ------
        
        Display a graph and a properties tuning window
        
        Example
        -------
        >>> import fbonnardot as fb; import numpy as np
        >>> data=np.array([[0,0,0,1,0],[1,2,1,0,0],[2,0,4,0,0],[3,0,0,6,0]])
        >>> fb.plotMatrix(data,0.1,2,'x','y','z')
        
        Warning
        -------
        Save your data before using this program : it can freeze Python
        """
        app = QtWidgets.QApplication.instance()
        if app is None:
            # Qt application does not run, so create it
            app = QtWidgets.QApplication([])   
            self.newapp=True
        else:
            # Qt application already running, so just show is sufficient
            self.newapp=False
            
        # Copy parameters to object instance
        self.data = data
        self.xlabel=xlabel
        self.ylabel=ylabel
        self.zlabel=zlabel
        # Creates x and y for plot 3D (add one line and column for pcolormesh)
        #   extra value is not used for other representations
        li,col=self.data.shape
        self.x=np.repeat([np.arange(col+1)],li+1,0)*stepx
        self.y=np.repeat(np.array([np.arange(li+1)]).T,col+1,1)*stepy
        # Creates the windows
        super(plotMatrix,self).__init__(None)
        self.makeWidgets()
        self.makeFigure2D()
        self.update()
        # Process events till end of program
        self.show()
        if self.newapp==True:
            # In case Qt application does not run
            app.exec_()

        
    def makeFigure(self,f3D):
        """Create a figure for display"""
        self.f3D=f3D
        # Creates the matplotlib figure
        self.fig=plt.Figure(figsize=(5, 4), dpi=100)
        if f3D:
            self.ax=self.fig.add_subplot(111,projection='3d')
        else:
            self.ax=self.fig.add_subplot(111)
        # Creates the dialog box with a Vertical Layout
        self.figdlg=QtWidgets.QDialog(self)
        self.figdlg.height=400
        self.figdlg.width=640
        self.vbl=QtWidgets.QVBoxLayout()
        self.figdlg.setLayout(self.vbl)
        # Creates Canvas i.e. a widget to display the figure in Qt5
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        # Creates a matplotlib toolbar
        self.toolbar = NavigationToolbar2QT(self.canvas,self.figdlg)
        self.toolbar.update()
        # Add these 2 widgets to vertical layout        
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        # Various actions
        self.canvas.draw()
        if f3D:
            self.ax.mouse_init()
        self.figdlg.show()
        
    def makeFigure2D(self):
        """Create a figure for 2D display"""
        self.makeFigure(False)

    def makeFigure3D(self):
        """Create a figure for 3D display"""
        self.makeFigure(True)
        
    def makeWidgets(self):
        """Setup windows widgets"""
        self.setObjectName("plotMatrix")
        self.setWindowTitle("plotMatrix")
        self.resize(296, 412)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # Frame to choose the scale
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText("Scale")
        self.verticalLayout.addWidget(self.label)
        self.selectSc = QtWidgets.QComboBox(self.centralwidget)
        self.selectSc.setObjectName("selectSc")
        self.selectSc.addItem("Linear")
        self.selectSc.addItem("Logarithmic (20.log10(abs))")
        self.verticalLayout.addWidget(self.selectSc)

        # Frame to choose the colormap
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Colormap")
        self.verticalLayout.addWidget(self.label_2)
        self.selectCm = QtWidgets.QComboBox(self.centralwidget)
        self.selectCm.setObjectName("selectCm")
        self.selectCm.addItem("plasma")
        self.selectCm.addItem("inferno")
        self.selectCm.addItem("Greys")
        self.selectCm.addItem("gray")
        self.selectCm.addItem("hsv")
        self.selectCm.addItem("jet")
        self.verticalLayout.addWidget(self.selectCm)

        # Frame to choose the type of representation
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Representation")
        self.verticalLayout.addWidget(self.label_3)
        self.selectRep = QtWidgets.QComboBox(self.centralwidget)
        self.selectRep.setObjectName("selectRep")
        self.selectRep.addItem("picture")
        self.selectRep.addItem("contours")
        self.selectRep.addItem("3D")
        self.selectRep.addItem("surface")
        self.verticalLayout.addWidget(self.selectRep)

        # Frame to choose thresholds
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Threshold")
        self.verticalLayout.addWidget(self.label_4)
        self.selectThL = QtWidgets.QSlider(self.centralwidget)
        self.selectThL.setOrientation(QtCore.Qt.Horizontal)
        self.selectThL.setObjectName("selectThL")
        self.verticalLayout.addWidget(self.selectThL)
        self.selectThH = QtWidgets.QSlider(self.centralwidget)
        self.selectThH.setOrientation(QtCore.Qt.Horizontal)
        self.selectThH.setObjectName("selectThH")
        self.verticalLayout.addWidget(self.selectThH)

        self.selectThL.setMinimum(0)
        self.selectThL.setMaximum(100)
        self.selectThL.setValue(0)
        
        self.selectThH.setMinimum(0)
        self.selectThH.setMaximum(100)
        self.selectThH.setValue(100)
        
        
        # Frame to choose min and max frequency
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("Displayed Frequency area")
        self.verticalLayout.addWidget(self.label_5)
        self.selectdfaL = QtWidgets.QSlider(self.centralwidget)
        self.selectdfaL.setOrientation(QtCore.Qt.Horizontal)
        self.selectdfaL.setObjectName("selectdfaL")
        self.verticalLayout.addWidget(self.selectdfaL)
        self.selectdfaH = QtWidgets.QSlider(self.centralwidget)
        self.selectdfaH.setOrientation(QtCore.Qt.Horizontal)
        self.selectdfaH.setObjectName("selectdfaH")
        self.verticalLayout.addWidget(self.selectdfaH)


        self.selectdfaL.setMinimum(0)
        self.selectdfaL.setMaximum(100)
        self.selectdfaL.setValue(0)
        
        self.selectdfaH.setMinimum(0)
        self.selectdfaH.setMaximum(100)
        self.selectdfaH.setValue(100)



        # frame with Button to update, create a new figure or quit
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btUp = QtWidgets.QPushButton(self.centralwidget)
        self.btUp.setObjectName("btUp")
        self.btUp.setText("Update Fig")
        self.horizontalLayout.addWidget(self.btUp)
        self.btNew = QtWidgets.QPushButton(self.centralwidget)
        self.btNew.setObjectName("btNew")
        self.btNew.setText("New Fig")
        self.horizontalLayout.addWidget(self.btNew)
        self.btQuit = QtWidgets.QPushButton(self.centralwidget)
        self.btQuit.setObjectName("btQuit")
        self.btQuit.setText("Quit")
        self.horizontalLayout.addWidget(self.btQuit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralwidget)

        #self.btQuit.clicked.connect(self.close)
        QtCore.QMetaObject.connectSlotsByName(self)
        
        
    def update(self):
        """Remove old plot and plot according new parameters"""
        # Read values choosen by user in dialog box
        sc=self.selectSc.currentIndex()
        cm=self.selectCm.currentText()
        rp=self.selectRep.currentIndex()
        thL=self.selectThL.value()
        thH=self.selectThH.value()
        dfaL=self.selectdfaL.value()
        dfaH=self.selectdfaH.value()
        self.ax.clear()
        
        # Change figure type if necessary (2D or 3D)
        if not self.f3D and rp>=2:
            self.figdlg.destroy()
            self.makeFigure3D()
            
        if self.f3D and rp<2:
            self.figdlg.destroy()
            self.makeFigure2D()    
            
        # Create a copy of data to apply threshold and log scale if asked
        data=np.array(self.data)
        
        mini=np.min(self.data)
        maxi=np.max(self.data)
        thLv=mini+(maxi-mini)*thL/100
        thHv=mini+(maxi-mini)*thH/100
        data[data<thLv]=thLv
        data[data>thHv]=thHv
        
        # Compute the frequency area to display
        ylimmin=self.y[0][0]+(self.y[-1][0]-self.y[0][0])*dfaL/100
        ylimmax=self.y[0][0]+(self.y[-1][0]-self.y[0][0])*dfaH/100
        
        if sc==1:
            data=20*np.log10(np.abs(data))
        
        # Display data
        if rp==0:
            self.ax.pcolormesh(self.x,self.y,data,cmap=cm)
            self.ax.set_ylim(bottom=ylimmin,top=ylimmax)
        elif rp==1:
            self.ax.contour(self.x[0:-1,0:-1],self.y[0:-1,0:-1],data,cmap=cm)
            self.ax.set_ylim(bottom=ylimmin,top=ylimmax)
        elif rp==2:
            self.ax.plot_wireframe(self.x[0:-1,0:-1],self.y[0:-1,0:-1],data)
            self.ax.set_ylim(bottom=ylimmin,top=ylimmax)
        elif rp==3:
            self.ax.plot_surface(self.x[0:-1,0:-1],self.y[0:-1,0:-1],data,cmap=cm)
            self.ax.set_ylim(bottom=ylimmin,top=ylimmax)

        # Give title to axes
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        if rp>=2:
            self.ax.set_zlabel(self.zlabel)
        
        # Ask to draw the figure contents
        self.canvas.draw()
        
    @QtCore.pyqtSlot()
    def on_btUp_clicked(self):
        self.update()

    @QtCore.pyqtSlot()
    def on_btNew_clicked(self):
        """Makes a new figure"""
        self.makeFigure2D()
        self.update()

    @QtCore.pyqtSlot()
    def on_btQuit_clicked(self):
        """Close all the windows to ends the application"""    
        self.close()
        if self.newapp==True:
            # Close application if it was not previously running
            QtWidgets.QApplication.closeAllWindows()
            QtWidgets.QApplication.exit()
        
    def closed(self):
        """Reacts to the close button on window bar (do not work everytime)"""
        #super().closed()
        if self.newapp==True:
            # Close application if it was not previously running
            QtWidgets.QApplication.closeAllWindows()
            QtWidgets.QApplication.exit()


# Auto-test if Python script launched from console ---------------------------
if __name__ == '__main__':
    print("Auto-test if Python script launched from console")
    print("You should see a dialog box to adjust options, and a graph.")
    pm=plotMatrix(np.array([[0,0,0,1,0],[1,2,1,0,0],[2,0,4,0,0],[3,0,0,6,0]]),0.1,2,'x','y','z')
    pm.show()
    
    



