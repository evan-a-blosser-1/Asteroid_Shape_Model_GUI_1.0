################
# GUI Capstone #
#########################
import GUI_packages as GP
##
import sys
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
###########################
from PySide6.QtCore import Slot,Qt
from PySide6.QtGui import QAction, QKeySequence
#from PyQt5.QtGui  import 
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout,
                               QHeaderView, QLabel, QMainWindow, QSlider,
                               QTableWidget, QVBoxLayout,
                               QWidget,QTextEdit)
#####################################
#
######################
# Define application ###########
class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        
        # Define Main widget
        self._main = QWidget()
        # Set as Central
        self.setCentralWidget(self._main)

        # Define the menu 
        self.menu = self.menuBar()
        # Add File 
        self.menu_file = self.menu.addMenu("File")
        exit = QAction("Exit", self, triggered=qApp.quit)
        self.menu_file.addAction(exit)
        
        # The About section
        self.menu_about = self.menu.addMenu("&About")
        about = QAction("About Qt", self, shortcut=QKeySequence(QKeySequence.HelpContents),
                        triggered=qApp.aboutQt)
        self.menu_about.addAction(about)

        ###################
        # Plotting Canvas #
        ###################
        # Figure (Left)
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)
        
        
        #################
        # Sliders (Left)
        min = 0
        max = 360
        self.slider_azim = QSlider(minimum=min, maximum=max, orientation=Qt.Horizontal)
        self.slider_elev = QSlider(minimum=min, maximum=max, orientation=Qt.Horizontal)

        self.slider_azim_layout = QHBoxLayout()
        self.slider_azim_layout.addWidget(QLabel(f"{min}"))
        self.slider_azim_layout.addWidget(self.slider_azim)
        self.slider_azim_layout.addWidget(QLabel(f"{max}"))

        self.slider_elev_layout = QHBoxLayout()
        self.slider_elev_layout.addWidget(QLabel(f"{min}"))
        self.slider_elev_layout.addWidget(self.slider_elev)
        self.slider_elev_layout.addWidget(QLabel(f"{max}"))
        ###################################################
        #
        ################################ 
        # Define Asteroid Info Display #
        ################################
        self.Asteroid_info = QTextEdit()
        #################

        ###########################
        # Asteroid Selection Menu #
        # ComboBox (Right)
        self.combo = QComboBox()
        self.combo.addItems(["Apophis",
                            "Arrokoth",
                            "Bilbo",
                            "Cerberus",
                            "Claudia",
                            "Danzig",
                            "Eva",
                            "Flora",
                            "Griffin",
                            "Hektor",
                             "Iris",
                             "Julia",
                             "Kleopatra",
                             "Lucifer",
                             "Mithra",
                             "Noviomagum",
                             "Otto",
                             "Persephone",
                             "Reinmuthia",
                             "Saville",
                             "Toutatis",
                             "Ursa",
                             "Vera",
                             "Waltraut",
                             "Xenia",
                             "Yeungchuchiu",
                             "Zoya"])
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

        ##############################
        # Signal and Slots connections
        self.combo.currentTextChanged.connect(self.combo_option)
        self.slider_azim.valueChanged.connect(self.rotate_azim)
        self.slider_elev.valueChanged.connect(self.rotate_elev)



###################################
 # Initial Plot set to be Apophis #
        self.Apophis()
        self._ax.view_init(30, 30)
        self.slider_azim.setValue(30)
        self.slider_elev.setValue(30)
        self.fig.canvas.mpl_connect("button_release_event", self.on_click)
        
    ##################
    # Define sliders #
    def on_click(self, event):
        azim, elev = self._ax.azim, self._ax.elev
        self.slider_azim.setValue(azim + 180)
        self.slider_elev.setValue(elev + 180)


    #####################################
    # Define The plot Canvas & Settings #
    def set_canvas_configuration(self):
        # Main FIX !!!
        # - clear figure for next plot
        self.fig.clf()
        ##############
        self.fig.set_canvas(self.canvas)
        self._ax = self.canvas.figure.add_subplot(projection="3d")
        # Axis Labels 
        self._ax.set_xlabel('km')
        self._ax.set_ylabel('km')
        self._ax.set_zlabel('km')
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
        #########################################  
    ####################################################### 
    
    ##########################
    ## Define Asteroid Plots #
    ##########################
    #
    ###########
    # Apophis #
    def Apophis(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Apophis_CM = GP.READ_IN('Apophis.out')
        self.X = Apophis_CM[:,0]
        self.Y = Apophis_CM[:,1]
        self.Z = Apophis_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Apophis.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ###########
    # Arrokoth #
    def Arrokoth(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Arrokoth_CM = GP.READ_IN('Arrokoth.out')
        self.X = Arrokoth_CM[:,0]
        self.Y = Arrokoth_CM[:,1]
        self.Z = Arrokoth_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Arrokoth.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ###########
    # Bilbo #
    def Bilbo(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Bilbo_CM = GP.READ_IN('Bilbo.out')
        self.X = Bilbo_CM[:,0]
        self.Y = Bilbo_CM[:,1]
        self.Z = Bilbo_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Bilbo.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ###########
    # Cerberus #
    def Cerberus(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Cerberus_CM = GP.READ_IN('Cerberus.out')
        self.X = Cerberus_CM[:,0]
        self.Y = Cerberus_CM[:,1]
        self.Z = Cerberus_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Cerberus.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ###########
    # Claudia #
    def Claudia(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Claudia_CM = GP.READ_IN('Claudia.out')
        self.X = Claudia_CM[:,0]
        self.Y = Claudia_CM[:,1]
        self.Z = Claudia_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Claudia.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ###########
    # Danzig #
    def Danzig(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Danzig_CM = GP.READ_IN('Danzig.out')
        self.X = Danzig_CM[:,0]
        self.Y = Danzig_CM[:,1]
        self.Z = Danzig_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Danzig.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ###########
    # Eva #
    def Eva(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Eva_CM = GP.READ_IN('Eva.out')
        self.X = Eva_CM[:,0]
        self.Y = Eva_CM[:,1]
        self.Z = Eva_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Eva.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ###########
    # Flora #
    def Flora(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Flora_CM = GP.READ_IN('Flora.out')
        self.X = Flora_CM[:,0]
        self.Y = Flora_CM[:,1]
        self.Z = Flora_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Flora.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ###########
    # Griffin #
    def Griffin(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Griffin_CM = GP.READ_IN('Griffin.out')
        self.X = Griffin_CM[:,0]
        self.Y = Griffin_CM[:,1]
        self.Z = Griffin_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Griffin.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ###########
    # Hektor  #
    def Hektor (self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Hektor_CM = GP.READ_IN('Hektor.out')
        self.X = Hektor_CM[:,0]
        self.Y = Hektor_CM[:,1]
        self.Z = Hektor_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Hektor.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Iris #
    def Iris(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Iris_CM = GP.READ_IN('Iris.out')
        self.X = Iris_CM[:,0]
        self.Y = Iris_CM[:,1]
        self.Z = Iris_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Iris.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Julia #
    def Julia(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Julia_CM = GP.READ_IN('Julia.out')
        self.X = Julia_CM[:,0]
        self.Y = Julia_CM[:,1]
        self.Z = Julia_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Julia.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Kleopatra #
    def Kleopatra(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Kleopatra_CM = GP.READ_IN('Kleopatra.out')
        self.X = Kleopatra_CM[:,0]
        self.Y = Kleopatra_CM[:,1]
        self.Z = Kleopatra_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Kleopatra.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Lucifer #
    def Lucifer(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Lucifer_CM = GP.READ_IN('Lucifer.out')
        self.X = Lucifer_CM[:,0]
        self.Y = Lucifer_CM[:,1]
        self.Z = Lucifer_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Lucifer.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Mithra #
    def Mithra(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Mithra_CM = GP.READ_IN('Mithra.out')
        self.X = Mithra_CM[:,0]
        self.Y = Mithra_CM[:,1]
        self.Z = Mithra_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Mithra.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Noviomagum #
    def Noviomagum(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Noviomagum_CM = GP.READ_IN('Noviomagum.out')
        self.X = Noviomagum_CM[:,0]
        self.Y = Noviomagum_CM[:,1]
        self.Z = Noviomagum_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Noviomagum.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Otto #
    def Otto(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Otto_CM = GP.READ_IN('Otto.out')
        self.X = Otto_CM[:,0]
        self.Y = Otto_CM[:,1]
        self.Z = Otto_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Otto.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Persephone #
    def Persephone(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Persephone_CM = GP.READ_IN('Persephone.out')
        self.X = Persephone_CM[:,0]
        self.Y = Persephone_CM[:,1]
        self.Z = Persephone_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Persephone.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Reinmuthia #
    def Reinmuthia(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Reinmuthia_CM = GP.READ_IN('Reinmuthia.out')
        self.X = Reinmuthia_CM[:,0]
        self.Y = Reinmuthia_CM[:,1]
        self.Z = Reinmuthia_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Reinmuthia.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Saville #
    def Saville(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Saville_CM = GP.READ_IN('Saville.out')
        self.X = Saville_CM[:,0]
        self.Y = Saville_CM[:,1]
        self.Z = Saville_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Saville.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Toutatis #
    def Toutatis(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Toutatis_CM = GP.READ_IN('Toutatis.out')
        self.X = Toutatis_CM[:,0]
        self.Y = Toutatis_CM[:,1]
        self.Z = Toutatis_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Toutatis.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Ursa #
    def Ursa(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Ursa_CM = GP.READ_IN('Ursa.out')
        self.X = Ursa_CM[:,0]
        self.Y = Ursa_CM[:,1]
        self.Z = Ursa_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Ursa.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Vera #
    def Vera(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Vera_CM = GP.READ_IN('Vera.out')
        self.X = Vera_CM[:,0]
        self.Y = Vera_CM[:,1]
        self.Z = Vera_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Vera.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Waltraut #
    def Waltraut(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Waltraut_CM = GP.READ_IN('Waltraut.out')
        self.X = Waltraut_CM[:,0]
        self.Y = Waltraut_CM[:,1]
        self.Z = Waltraut_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Waltraut.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Xenia #
    def Xenia(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Xenia_CM = GP.READ_IN('Xenia.out')
        self.X = Xenia_CM[:,0]
        self.Y = Xenia_CM[:,1]
        self.Z = Xenia_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Xenia.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Yeungchuchiu #
    def Yeungchuchiu(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Yeungchuchiu_CM = GP.READ_IN('Yeungchuchiu.out')
        self.X = Yeungchuchiu_CM[:,0]
        self.Y = Yeungchuchiu_CM[:,1]
        self.Z = Yeungchuchiu_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Yeungchuchiu.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    #
    ########
    # Zoya #
    def Zoya(self):
        # Call plot settings
        self.set_canvas_configuration()
        # Assign Asteroid Data
        Zoya_CM = GP.READ_IN('Zoya.out')
        self.X = Zoya_CM[:,0]
        self.Y = Zoya_CM[:,1]
        self.Z = Zoya_CM[:,2]
        # Plot Asteroid
        self._ax.scatter3D(self.X,self.Y,self.Z,
               marker='.',
               color='#D41159')
        self.canvas.draw()
        # Set Asteroid Information out
        with open("Zoya.txt", "r") as file:
                Output_Message = file.read()
                self.Asteroid_info.setText(Output_Message)
    #################################################
    
    
    
    ###############################
    # Slot for Asteroid selection #
    @Slot()
    def combo_option(self, text):
        if text == "Apophis":
            self.Apophis()
        elif text == "Arrokoth":
            self.Arrokoth()
        elif text == "Bilbo":
            self.Bilbo()
        elif text == "Cerberus":
            self.Cerberus() 
        elif text == "Claudia":
            self.Claudia()   
        elif text == "Danzig":
            self.Danzig()  
        elif text == "Eva":
            self.Eva() 
        elif text == "Flora":
            self.Flora() 
        elif text == "Griffin":
            self.Griffin() 
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
        elif text =="Reinmuthia":
            self.Reinmuthia()
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
#################################        
#####
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
