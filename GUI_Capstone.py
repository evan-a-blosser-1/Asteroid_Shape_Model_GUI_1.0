################
# GUI Capstone #
#########################
import GUI_packages as GP
##
import sys
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
###########################
from PySide6.QtCore import Slot,Qt
from PySide6.QtGui import QAction, QKeySequence
#from PyQt5.QtGui  import 
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout,
                               QHeaderView, QLabel, QMainWindow, QSlider,
                               QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget)
#####################################
#
######################
# Define application ###########
class ApplicationWindow(QMainWindow):
    def __init__(Window, parent=None):
        QMainWindow.__init__(Window, parent)
        
        
        # Set s labels for right hand table
        Window.column_names = ["Column A", "Column B", "Column C"]

        # Define Main widget
        Window._main = QWidget()
        # Set as Central
        Window.setCentralWidget(Window._main)

        # Define the menu 
        Window.menu = Window.menuBar()
        # Add File 
        Window.menu_file = Window.menu.addMenu("File")
        exit = QAction("Exit", Window, triggered=qApp.quit)
        Window.menu_file.addAction(exit)

        Window.menu_about = Window.menu.addMenu("&About")
        about = QAction("About Qt", Window, shortcut=QKeySequence(QKeySequence.HelpContents),
                        triggered=qApp.aboutQt)
        Window.menu_about.addAction(about)

        # Figure (Left)
        Window.fig = Figure(figsize=(5, 3))
        Window.canvas = FigureCanvas(Window.fig)

        # Sliders (Left)
        min = 0
        max = 360
        Window.slider_azim = QSlider(minimum=min, maximum=max, orientation=Qt.Horizontal)
        Window.slider_elev = QSlider(minimum=min, maximum=max, orientation=Qt.Horizontal)

        Window.slider_azim_layout = QHBoxLayout()
        Window.slider_azim_layout.addWidget(QLabel(f"{min}"))
        Window.slider_azim_layout.addWidget(Window.slider_azim)
        Window.slider_azim_layout.addWidget(QLabel(f"{max}"))

        Window.slider_elev_layout = QHBoxLayout()
        Window.slider_elev_layout.addWidget(QLabel(f"{min}"))
        Window.slider_elev_layout.addWidget(Window.slider_elev)
        Window.slider_elev_layout.addWidget(QLabel(f"{max}"))

        # Table (Right)
        Window.table = QTableWidget()
        header = Window.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # ComboBox (Right)
        Window.combo = QComboBox()
        Window.combo.addItems(["Apophis","Iris"])

        # Right layout
        rlayout = QVBoxLayout()
        rlayout.setContentsMargins(1, 1, 1, 1)
        rlayout.addWidget(QLabel("Plot type:"))
        rlayout.addWidget(Window.combo)
        rlayout.addWidget(Window.table)

        # Left layout
        llayout = QVBoxLayout()
        rlayout.setContentsMargins(1, 1, 1, 1)
        llayout.addWidget(Window.canvas, 88)
        llayout.addWidget(QLabel("Azimuth:"), 1)
        llayout.addLayout(Window.slider_azim_layout, 5)
        llayout.addWidget(QLabel("Elevation:"), 1)
        llayout.addLayout(Window.slider_elev_layout, 5)

        # Main layout
        layout = QHBoxLayout(Window._main)
        layout.addLayout(llayout, 70)
        layout.addLayout(rlayout, 30)

        # Signal and Slots connections
        Window.combo.currentTextChanged.connect(Window.combo_option)
        Window.slider_azim.valueChanged.connect(Window.rotate_azim)
        Window.slider_elev.valueChanged.connect(Window.rotate_elev)




######################################
 # Initial setup
        Window.Apophis()
        Window._ax.view_init(30, 30)
        Window.slider_azim.setValue(30)
        Window.slider_elev.setValue(30)
        Window.fig.canvas.mpl_connect("button_release_event", Window.on_click)
        
 # Matplotlib slot method
    def on_click(Window, event):
        azim, elev = Window._ax.azim, Window._ax.elev
        Window.slider_azim.setValue(azim + 180)
        Window.slider_elev.setValue(elev + 180)

    # Utils methods

    def set_table_data(Window, X, Y, Z):
        for i in range(len(X)):
            Window.table.setItem(i, 0, QTableWidgetItem(f"{X[i]:.2f}"))
            Window.table.setItem(i, 1, QTableWidgetItem(f"{Y[i]:.2f}"))
            Window.table.setItem(i, 2, QTableWidgetItem(f"{Z[i]:.2f}"))

    def set_canvas_table_configuration(Window, row_count, data):
        Window.fig.set_canvas(Window.canvas)
        Window._ax = Window.canvas.figure.add_subplot(projection="3d")

        Window._ax.set_xlabel(Window.column_names[0])
        Window._ax.set_ylabel(Window.column_names[1])
        Window._ax.set_zlabel(Window.column_names[2])

        Window.table.setRowCount(row_count)
        Window.table.setColumnCount(3)
        Window.table.setHorizontalHeaderLabels(Window.column_names)
        Window.set_table_data(data[0], data[1], data[2])

    # Plot methods
    def Apophis(Window):
        Window.fig.set_canvas(Window.canvas)
        Window._ax = Window.canvas.figure.add_subplot(projection="3d")
        Apophis_CM = GP.READ_IN('Apophis.out')
        Window.X = Apophis_CM[:,0]
        Window.Y = Apophis_CM[:,1]
        Window.Z = Apophis_CM[:,2]
        
        Window._ax.scatter3D(Window.X,Window.Y,Window.Z,
               marker='.',
               color='red')

        Window.canvas.draw()
        
    def Iris(Window):
        Iris_CM = GP.READ_IN('Iris.out')
        Window.X = Iris_CM[:,0]
        Window.Y = Iris_CM[:,1]
        Window.Z = Iris_CM[:,2]
        
        Window._ax.scatter3D(Window.X,Window.Y,Window.Z,
               marker='.',
               color='red')

        Window.canvas.draw()
   
    # Slots

    @Slot()
    def combo_option(Window, text):
        if text == "Apophis":
            Window.Apophis()
        elif text =="Iris":
            Window.Iris()
      


    @Slot()
    def rotate_azim(Window, value):
        Window._ax.view_init(Window._ax.elev, value)
        Window.fig.set_canvas(Window.canvas)
        Window.canvas.draw()

    @Slot()
    def rotate_elev(Window, value):
        Window._ax.view_init(value, Window._ax.azim)
        Window.fig.set_canvas(Window.canvas)
        Window.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ApplicationWindow()
    w.setFixedSize(1280, 720)
    w.show()
    app.exec()
