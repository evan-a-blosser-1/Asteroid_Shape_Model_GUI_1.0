# Asteroid_Shape_Model_GUI_1.0
This is the repository for my OU Engineering Physics Capstone Project 

---

## MAIN_GUI

  contains all the necessary files, simply run `Asteroids_In_MASCON.py` in your favorite Interactive Development Environment (IDE)!

---

## Installing `Asteroids_In_MASCON`
  The `Asteroids_In_MASCON_Setup.exe` can be downloaded from the "Releases" tab located on the right of this page.
  The current release is **Version_1.3**

  1. Download the `Asteroids_In_MASCON_Setup.exe` file
  2. Locate the file and run as administrator
      - Windows will warn you that I am an Unknown publisher:
        
        ![image](https://github.com/evan-a-blosser-1/Asteroid_Shape_Model_GUI_1.0/assets/85218360/5bf24413-4d60-49d8-91e0-4affb43f8df8)
        
      - Simply click **more info** and then **Run anyway**:
        
        ![image](https://github.com/evan-a-blosser-1/Asteroid_Shape_Model_GUI_1.0/assets/85218360/0aae3d60-67a4-434b-8a8f-d52984f1683f)
        
3. Next just follow the setup you can choose where to install, and if you want a desktop shortcut.

   - I recommend creating the shortcut for ease of locating the software. 

---

## obj2MirtichData.py
  This is a program that can take a .obj file and convert it to a format that can be run inside `volInt.c`

### volInt.c
  Created by Brian Mirtich, and can be found at:  
  
    https://github.com/OpenFOAM/OpenFOAM-2.1.x/blob/master/src/meshTools/momentOfInertia/volumeIntegration/volInt.c 

---

## Asteroid_CM

  A universal software developed to process shape models in OBJ format. Returns a file of positional data of each calculated Center of Mass for the tetrahedrons that make the polyhedron shape model. 

  This also has a method for scaling the shape model using a mean radius that can either be input by the user, or you can select to not scale the shape model. 

---

## Apophis Recreation

  Contains preliminary work on the asteroid model Apophis, to calculate the Center of Masses for each tetrahedron within the polyhedron shape model (.obj file).

---

## Mean_Radius_CCalculations.ipynb

  Contains a log of mean radius and scaling done for all asteroids within this project.
