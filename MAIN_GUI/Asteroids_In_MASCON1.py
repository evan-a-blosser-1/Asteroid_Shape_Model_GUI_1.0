"""
Program: Asteroids_In_MASCON1.py
Description: GUI that displays asteroid shape models
                along with the Center of Masses for the 
                shapes tetrahedrons; represented as 
                as the layer of points. This shows the points
                used to caclualte teh gravity potentail in 
                MASCON I.

MIT License

Copyright (c) [2023] [Evan Blosser]

"""

###################
# Import Packages #
#########################
# File reading
import GUI_packages as GP
# System basics
import sys
# Mathmatical !!
import numpy as np
# Import pyplot as plt from matplotlib
import matplotlib.pyplot as plt
#
###############
# GUI Pckages #
###############
# Import GUI supported Canvas from matplotlob
from matplotlib.backends.backend_qtagg import FigureCanvas
# Import matplotlib built in tool bar
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar
# Import figure from matplotlib
from matplotlib.figure import Figure
# Import 3D axes for 3D plotting
from mpl_toolkits.mplot3d import axes3d
###########################
# Import Qt & Selection slots
from PySide6.QtCore import Slot,Qt
# Import Tool bar buttons & Font for user text
from PySide6.QtGui import QAction, QKeySequence, QFont
# Imports:
#  - Application window
#  - Display boxs & headers
#  - layout funcitons
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel, 
                               QMainWindow, QSlider, QVBoxLayout,QWidget,
                               QTextEdit,QMessageBox)
#####################################
#
######################
# Define application #
######################
class ApplicationWindow(QMainWindow):
    # Define main window
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        # Define Main widget
        self._main = QWidget()
        # Set as Central
        self.setCentralWidget(self._main)
        ###############
        ## Main Menu ##
        ###############
        # Define menu bar
        self.menu = self.menuBar()
        
        # Add File 
        self.menu_file = self.menu.addMenu("File")
        exit = QAction("Exit", self, triggered=qApp.quit)
        self.menu_file.addAction(exit)
        
        
        ##################
        # About Software #
        ##################
        # Define about section of menu
        self.menu_about = self.menu.addMenu("&About")
        # Define about message box
        def About_Message():
            # Call message file
            with open("Other_Info/About.md", "r") as file:
                Output_Message = file.read()
                msg_box = QMessageBox()
                msg_box.setWindowTitle("About")
                msg_box.setText(Output_Message)
                msg_box.exec()
        # Assign about in menu
        about = QAction("About", self, shortcut=QKeySequence(QKeySequence.HelpContents),
                        triggered=About_Message)
        self.menu_about.addAction(about)
        ################################
        #
        ###############
        # MIT License #
        ###############
        # Define License message box
        def MIT_License():
            # Call message file
            with open("Other_Info/MIT_License_Evan.md", "r") as file:
                Output_Message = file.read()
                msg_box = QMessageBox()
                msg_box.setWindowTitle("MIT License")
                msg_box.setText(Output_Message)
                msg_box.exec()
        # Assign license in menu
        License = QAction("License", self, shortcut=QKeySequence(QKeySequence.HelpContents),
                        triggered=MIT_License)
        self.menu_about.addAction(License)
        ##################################
        #
        ###################
        # Plotting Canvas #
        ###################
        # Define figure & canvas
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)
        # Embed Matplotlib toolbar
        self.toolbar = NavBar(self.canvas, self)
        ###################################################
        #
        ###############
        # Set Sliders #
        ###############
        # Define minimum and maximum rotation from 0 to 360 degrees
        min = 0
        max = 360
        # Azimuth Slider
        self.slider_azim = QSlider(minimum=min, maximum=max, orientation=Qt.Horizontal)
        self.slider_azim_layout = QHBoxLayout()
        self.slider_azim_layout.addWidget(QLabel(f"{min}"))
        self.slider_azim_layout.addWidget(self.slider_azim)
        self.slider_azim_layout.addWidget(QLabel(f"{max}"))
        # Elevation Slider
        self.slider_elev = QSlider(minimum=min, maximum=max, orientation=Qt.Horizontal)
        self.slider_elev_layout = QHBoxLayout()
        self.slider_elev_layout.addWidget(QLabel(f"{min}"))
        self.slider_elev_layout.addWidget(self.slider_elev)
        self.slider_elev_layout.addWidget(QLabel(f"{max}"))
        ###################################################
        #
        ################################ 
        # Define Asteroid Info Display #
        #####################################
        # Set Asteroid information          #
        self.Asteroid_info = QTextEdit()    #
        # Set Font and Size                 #
        font = QFont('Times New Roman', 14) #
        # Apply to Asteroid information     #
        self.Asteroid_info.setFont(font)    #
        #####################################
        #
        ###########################
        # Asteroid Selection Menu #
        ###########################
        # Define combo box
        self.combo = QComboBox()
        self.combo.addItems(["Welcome","Apophis", "Arrokoth", "Bilbo",
                            "Cerberus", "Danzig","Eva", "Flora", 
                            "Geographos","Hektor", "Iris", "Julia",
                             "Kleopatra", "Lucifer", "Mithra",
                             "Noviomagum", "Otto", "Persephone",
                             "Runcorn", "Saville", "Toutatis",
                             "Ursa", "Vera", "Waltraut",
                             "Xenia", "Yeungchuchiu","Zoya"])
        ######################################################
        #
        #################
        # Window Layout #
        #################
        # Right layout
        rlayout = QVBoxLayout()
        rlayout.setContentsMargins(1, 1, 1, 1)
        rlayout.addWidget(QLabel("Please select an Asteroid from the drop down menu:"))
        rlayout.addWidget(self.combo)
        rlayout.addWidget(self.Asteroid_info)

        # Left layout
        llayout = QVBoxLayout()
        llayout.addWidget(self.toolbar)
        rlayout.setContentsMargins(1, 1, 1, 1)
        llayout.addWidget(self.canvas, 88)
        llayout.addWidget(QLabel("Azimuth:"), 1)
        llayout.addLayout(self.slider_azim_layout, 5)
        llayout.addWidget(QLabel("Elevation:"), 1)
        llayout.addLayout(self.slider_elev_layout, 5)
       
        # Main layout
        layout = QHBoxLayout(self._main)
        layout.addLayout(llayout, 70)
        layout.addLayout(rlayout, 30)

        ################################
        # Signal and Slots connections ########################
        self.combo.currentTextChanged.connect(self.combo_option)
        self.slider_azim.valueChanged.connect(self.rotate_azim)
        self.slider_elev.valueChanged.connect(self.rotate_elev)
        #######################################################
        #
        ##################################
        # Initial Plot set to be Apophis #
        ##################################
        # Call configuration
        self.set_canvas_configuration()
        # Plot Apophis initially 
        self.draw_blank()
        # Set initial values for Azimuth & Elevation
        self._ax.view_init(30, 30)
        self.slider_azim.setValue(30)
        self.slider_elev.setValue(30)
        self.fig.canvas.mpl_connect("button_release_event", self.on_click)
        ##################################################################
        #
    ##################
    # Define sliders #
    ##################
    def on_click(self, event):
        azim, elev = self._ax.azim, self._ax.elev
        self.slider_azim.setValue(azim + 180)
        self.slider_elev.setValue(elev + 180)
    #########################################
    #
    #####################################
    # Define The plot Canvas & Settings #
    #####################################
    def set_canvas_configuration(self):
        # Main FIX !!!
        # - clear figure for next plot
        self.fig.clf()
        ##############
        self.fig.set_canvas(self.canvas)
        self._ax = self.canvas.figure.add_subplot(projection="3d")
        # Axis Labels 
        self._ax.set_xlabel('X (km)')
        self._ax.set_ylabel('Y (km)')
        self._ax.set_zlabel('Z (km)')
        # Set initial plot zoom
        self._ax.margins(0.42)
        ##########
        # Colors ###############
        Space      = "#000000" # Space Backdrop
        Grid_Color = '#1A85FF' # Blue for colorblind
        ########################
        # Background Color                           
        self.fig.set_facecolor(Space)                
        self._ax.set_facecolor(Space)                
        # Grid Pane Color/set to clear               
        self._ax.xaxis.set_pane_color((0.0, 0.0,     
                                    0.0, 0.0))       
        self._ax.yaxis.set_pane_color((0.0, 0.0,     
                                    0.0, 0.0))       
        self._ax.zaxis.set_pane_color((0.0, 0.0,     
                                    0.0, 0.0))       
        # Grid Ticks & Axis Colors 
        self._ax.tick_params(axis='x', colors=Grid_Color) 
        self._ax.tick_params(axis='y', colors=Grid_Color) 
        self._ax.tick_params(axis='z', colors=Grid_Color) 
        self._ax.yaxis.label.set_color(Grid_Color)        
        self._ax.xaxis.label.set_color(Grid_Color)        
        self._ax.zaxis.label.set_color(Grid_Color)        
        self._ax.xaxis.line.set_color(Grid_Color)         
        self._ax.yaxis.line.set_color(Grid_Color)         
        self._ax.zaxis.line.set_color(Grid_Color)     
        # Grid Line Color                            
        plt.rcParams['grid.color'] = Grid_Color
    ####################################################### 
    #
    #################################
    # Define Welcome message & Plot #
    #################################
    
    def draw_blank(self):
         # Call plot settings
        self.set_canvas_configuration()
        
        self.canvas.draw()
        # Set Welcome message in Asteroid info box
        with open("Other_Info/Welcome.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    ##########################
    ## Define Asteroid Plots #
    ##########################
    #
    ###########
    # Apophis ########
    def Apophis(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Read in calculated Center of Masses
        Apophis_CM = GP.READ_IN('Asteroid_CM/Apophis.out')
        # Assign Asteroid Data
        self.X = Apophis_CM[:,0]
        self.Y = Apophis_CM[:,1]
        self.Z = Apophis_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale =  0.23884078666393335
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Apophis.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Apophis.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    ########################################################
    #
    ############
    # Arrokoth ########
    def Arrokoth(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Arrokoth_CM = GP.READ_IN('Asteroid_CM/Arrokoth.out')
        self.X = Arrokoth_CM[:,0]
        self.Y = Arrokoth_CM[:,1]
        self.Z = Arrokoth_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 1.003738848598423
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Arrokoth.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Arrokoth.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    #########
    # Bilbo ########
    def Bilbo(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Bilbo_CM = GP.READ_IN('Asteroid_CM/Bilbo.out')
        self.X = Bilbo_CM[:,0]
        self.Y = Bilbo_CM[:,1]
        self.Z = Bilbo_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 5.100563165342119
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Bilbo.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Bilbo.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ############
    # Cerberus ########
    def Cerberus(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Cerberus_CM = GP.READ_IN('Asteroid_CM/Cerberus.out')
        self.X = Cerberus_CM[:,0]
        self.Y = Cerberus_CM[:,1]
        self.Z = Cerberus_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 0.4700320526985952
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Cerberus.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Cerberus.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ##########
    # Danzig ########
    def Danzig(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Danzig_CM = GP.READ_IN('Asteroid_CM/Danzig.out')
        self.X = Danzig_CM[:,0]
        self.Y = Danzig_CM[:,1]
        self.Z = Danzig_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 9.273520448812137
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Danzig.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]])  
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Danzig.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    #######
    # Eva ########
    def Eva(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Eva_CM = GP.READ_IN('Asteroid_CM/Eva.out')
        self.X = Eva_CM[:,0]
        self.Y = Eva_CM[:,1]
        self.Z = Eva_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 74.20189405027513
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Eva.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]])  
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Eva.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    #########
    # Flora ########
    def Flora(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Flora_CM = GP.READ_IN('Asteroid_CM/Flora.out')
        self.X = Flora_CM[:,0]
        self.Y = Flora_CM[:,1]
        self.Z = Flora_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 1.0161368060728935
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Flora.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Flora.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ##############
    # Geographos ########
    def Geographos(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Geographos_CM = GP.READ_IN('Asteroid_CM/Geographos.out')
        self.X = Geographos_CM[:,0]
        self.Y = Geographos_CM[:,1]
        self.Z = Geographos_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 0.8604483326862341
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Geographos.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Geographos.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ##########
    # Hektor #########
    def Hektor (self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Hektor_CM = GP.READ_IN('Asteroid_CM/Hektor.out')
        self.X = Hektor_CM[:,0]
        self.Y = Hektor_CM[:,1]
        self.Z = Hektor_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 125.1552869904105
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Hektor.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Hektor.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ########
    # Iris ########
    def Iris(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Iris_CM = GP.READ_IN('Asteroid_CM/Iris.out')
        self.X = Iris_CM[:,0]
        self.Y = Iris_CM[:,1]
        self.Z = Iris_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 0.9397839352627169
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Iris.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Iris.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    #########
    # Julia ########
    def Julia(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Julia_CM = GP.READ_IN('Asteroid_CM/Julia.out')
        self.X = Julia_CM[:,0]
        self.Y = Julia_CM[:,1]
        self.Z = Julia_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale =  0.9015971003020035
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Julia.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Julia.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    #############
    # Kleopatra #######
    def Kleopatra(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Kleopatra_CM = GP.READ_IN('Asteroid_CM/Kleopatra.out')
        self.X = Kleopatra_CM[:,0]
        self.Y = Kleopatra_CM[:,1]
        self.Z = Kleopatra_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 0.8133640395837609
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Kleopatra.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Kleopatra.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ###########
    # Lucifer ########
    def Lucifer(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Lucifer_CM = GP.READ_IN('Asteroid_CM/Lucifer.out')
        self.X = Lucifer_CM[:,0]
        self.Y = Lucifer_CM[:,1]
        self.Z = Lucifer_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 21.57712545847271
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Lucifer.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Lucifer.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ##########
    # Mithra ########
    def Mithra(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Mithra_CM = GP.READ_IN('Asteroid_CM/Mithra.out')
        self.X = Mithra_CM[:,0]
        self.Y = Mithra_CM[:,1]
        self.Z = Mithra_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 1.1245972680856962
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Mithra.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Mithra.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ##############
    # Noviomagum ########
    def Noviomagum(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Noviomagum_CM = GP.READ_IN('Asteroid_CM/Noviomagum.out')
        self.X = Noviomagum_CM[:,0]
        self.Y = Noviomagum_CM[:,1]
        self.Z = Noviomagum_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 1.061747242223572
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Noviomagum.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Noviomagum.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ########
    # Otto ########
    def Otto(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Otto_CM = GP.READ_IN('Asteroid_CM/Otto.out')
        self.X = Otto_CM[:,0]
        self.Y = Otto_CM[:,1]
        self.Z = Otto_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 10.89637979719658
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Otto.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]])  
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Otto.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ##############
    # Persephone ########
    def Persephone(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Persephone_CM = GP.READ_IN('Asteroid_CM/Persephone.out')
        self.X = Persephone_CM[:,0]
        self.Y = Persephone_CM[:,1]
        self.Z = Persephone_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 26.54152271850921
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Persephone.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]])  
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Persephone.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ###########
    # Runcorn ########
    def Runcorn(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Runcorn_CM = GP.READ_IN('Asteroid_CM/Runcorn.out')
        self.X = Runcorn_CM[:,0]
        self.Y = Runcorn_CM[:,1]
        self.Z = Runcorn_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 2.502147296572005
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Runcorn.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]])  
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Runcorn.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ###########
    # Saville ########
    def Saville(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Saville_CM = GP.READ_IN('Asteroid_CM/Saville.out')
        self.X = Saville_CM[:,0]
        self.Y = Saville_CM[:,1]
        self.Z = Saville_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 4.9301903600949455
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Saville.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]])  
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Saville.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ############
    # Toutatis ########
    def Toutatis(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Toutatis_CM = GP.READ_IN('Asteroid_CM/Toutatis.out')
        self.X = Toutatis_CM[:,0]
        self.Y = Toutatis_CM[:,1]
        self.Z = Toutatis_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 1.7910733773064786
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Toutatis.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]])  
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Toutatis.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ########
    # Ursa ########
    def Ursa(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Ursa_CM = GP.READ_IN('Asteroid_CM/Ursa.out')
        self.X = Ursa_CM[:,0]
        self.Y = Ursa_CM[:,1]
        self.Z = Ursa_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 22.92297044211607
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Ursa.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Ursa.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ########
    # Vera ########
    def Vera(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Vera_CM = GP.READ_IN('Asteroid_CM/Vera.out')
        self.X = Vera_CM[:,0]
        self.Y = Vera_CM[:,1]
        self.Z = Vera_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 55.18763465915349
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Vera.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]])  
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Vera.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ############
    # Waltraut ########
    def Waltraut(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Waltraut_CM = GP.READ_IN('Asteroid_CM/Waltraut.out')
        self.X = Waltraut_CM[:,0]
        self.Y = Waltraut_CM[:,1]
        self.Z = Waltraut_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 18.50441901028305
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Waltraut.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Waltraut.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    #########
    # Xenia ########
    def Xenia(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Xenia_CM = GP.READ_IN('Asteroid_CM/Xenia.out')
        self.X = Xenia_CM[:,0]
        self.Y = Xenia_CM[:,1]
        self.Z = Xenia_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 18.729161655946683
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Xenia.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Xenia.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ################
    # Yeungchuchiu ########
    def Yeungchuchiu(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Yeungchuchiu_CM = GP.READ_IN('Asteroid_CM/Yeungchuchiu.out')
        self.X = Yeungchuchiu_CM[:,0]
        self.Y = Yeungchuchiu_CM[:,1]
        self.Z = Yeungchuchiu_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 7.9518021638388
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Yeungchuchiu.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Yeungchuchiu.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ########
    # Zoya ########
    def Zoya(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Zoya_CM = GP.READ_IN('Asteroid_CM/Zoya.out')
        self.X = Zoya_CM[:,0]
        self.Y = Zoya_CM[:,1]
        self.Z = Zoya_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        # Correct asteroid distacnce units scale
        scale = 5.321921105048268
        # Read in OBJ file and assign as a 3D mesh of faces
        Asteroid_Mesh = GP.OBJ_READ_IN('OBJ_Files/Zoya.obj',scale)
        # Add outside faces as 3D mesh
        self._ax.add_collection3d(Asteroid_Mesh) 
        # Set Asteroid Aspect Ratio 
        self._ax.set_box_aspect(                                   
            [np.ptp(coord) for coord in [self.X, self.Y, self.Z]]) 
        # Draw Asteroid
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Asteroid_Info/Zoya.md", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setMarkdown(Output_Message)
    #################################################
    #
    ###############################
    # Slot for Asteroid selection #
    @Slot()
    def combo_option(self, text):
        if text == "Apophis":
            self.Apophis()
        elif text == "Welcome":
            self.draw_blank()
        elif text == "Arrokoth":
            self.Arrokoth()
        elif text == "Bilbo":
            self.Bilbo()
        elif text == "Cerberus":
            self.Cerberus() 
        elif text == "Danzig":
            self.Danzig()  
        elif text == "Eva":
            self.Eva() 
        elif text == "Flora":
            self.Flora() 
        elif text == "Geographos":
            self.Geographos() 
        elif text == "Hektor":
            self.Hektor() 
        elif text =="Iris":
            self.Iris()
        elif text =="Julia":
            self.Julia()
        elif text =="Kleopatra":
            self.Kleopatra()
        elif text =="Lucifer":
            self.Lucifer()
        elif text =="Mithra":
            self.Mithra()
        elif text =="Noviomagum":
            self.Noviomagum()
        elif text =="Otto":
            self.Otto()
        elif text =="Persephone":
            self.Persephone()
        elif text =="Runcorn":
            self.Runcorn()
        elif text =="Saville":
            self.Saville()
        elif text =="Toutatis":
            self.Toutatis()
        elif text =="Ursa":
            self.Ursa()
        elif text =="Vera":
            self.Vera()
        elif text =="Waltraut":
            self.Waltraut()
        elif text =="Xenia":
            self.Xenia()
        elif text =="Yeungchuchiu":
            self.Yeungchuchiu()
        elif text =="Zoya":
            self.Zoya()
    ############################### 
    #       
    ###########################
    # Slots for Azim. & Elev. #
    ###########################
    @Slot()
    def rotate_azim(self, value):
        self._ax.view_init(self._ax.elev, value)
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()
    @Slot()
    def rotate_elev(self, value):
        self._ax.view_init(value, self._ax.azim)
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()
#######################
# Execute the Program #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ApplicationWindow()
    w.show()
    app.exec()
