"""
Program: Asteroids_In_MASCON1.py
Description: Calculates the Center of mass in MASCON 1
                -Uses Mean Radius based scaling. 

MIT License

Copyright (c) [2023] [Evan Blosser]

"""

import sys
import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
#
###############
# User Inputs #
###############################################################
# Ask for Desired File Name                                   
Asteroid_file_in = input('|Please input desired file name: ') 
# Add .obj extension to file name                             
Asteroid_file = (Asteroid_file_in +'.obj')
# User input instruction
USER_MESSAGE_CM_INPUT =f'''
{'-'*42}
|  For the following inputs please enter each of the
|   calculated Center of Mass values as prompted
{'-'*42}
'''
print(USER_MESSAGE_CM_INPUT)
CM_input_X  = float(input('|Please input the x-coordinate: '))
CM_input_Y  = float(input('|Please input the y-coordinate: '))
CM_input_Z  = float(input('|Please input the z-coordinate: '))
CM = np.array([CM_input_X,CM_input_Y,CM_input_Z])
###############################################################
#
#######################
# Load ,txt data file ###################################### 
data = np.loadtxt(Asteroid_file, delimiter=' ', dtype=str) #
############################################################
###############################################################
# Set Vertex/Faces denotaed as v or f in .obj format to array #
vertex_faces = data[:,0]                                      #
# Get Length of the Vertex/Faces array for range counting     #
V_F_Range = vertex_faces.size                                 #
# Define varibale for number of vertices & faces              #
numb_vert = 0                                                 #
numb_face = 0                                                 #
# Scan Data for v & f and count the numbers of each.          #
#  Used for sorting x, y, & z as vertices                     #
for i in range(0,V_F_Range):                                  #
    if vertex_faces[i] == 'v':                                #
        numb_vert += 1                                        #
    else:                                                     #
        numb_face += 1                                        #
###############################################################
#########################
# Assigning Vertex Data #
#########################
# Vertex data assigned to x, y, & z
#  then cpnverts to float type
########################################
# Assign 2nd row of .txt as x input    #
x_input = data[range(0,numb_vert),1]   #
# Assign 3rd row of .txt as y input    #
y_input = data[range(0,numb_vert),2]   #
# Assign 4th row of .txt as z input    #
z_input = data[range(0,numb_vert),3]   #
# Convert Vertices data to float type  #
x_0 = x_input.astype(float)            #
y_0 = y_input.astype(float)            #
z_0 = z_input.astype(float)            #
########################################
#
##############################################
# Fill zero indecies with dummy values       #
#  to allow faces to call vertices 1 to 1014 #
x = np.append(0,x_0)  ########################
y = np.append(0,y_0)  #
z = np.append(0,z_0)  #
#######################
#
#######################
# Assigning Face Data #
#######################
# Face data assigned to fx, fy, & fz
#  then cpnverts to float type
#############################################
# Range count for face data                 #
row_tot = numb_face + numb_vert             #
# Assign 2nd row of .txt as x input         #
fx_input = data[range(numb_vert,row_tot),1] #
# Assign 3rd row of .txt as y input         #
fy_input = data[range(numb_vert,row_tot),2] #
# Assign 4th row of .txt as z input         #
fz_input = data[range(numb_vert,row_tot),3] #
# Convert Vertices data to float type       #
fx = fx_input.astype(int)                   #
fy = fy_input.astype(int)                  #
fz = fz_input.astype(int)                 #
##########################################
#
##########################
# Creating Output Arrays #
##########################
#    Number of Vertex is (N-1)             
#     numb_vert += 1
#########################################
# Number of Vertex set to array         #
numb_vert_array = []                    #
numb_vert_array.append(numb_vert)       #
# Number of Faces set to array          #
numb_face_array = []                    #
numb_face_array.append(numb_face)       #
# Stacking Columns of Vertex Data       #################
Vert_Data_Out_0 = np.column_stack((x, y))               #
Vert_Data       = np.column_stack((Vert_Data_Out_0, z)) #
# Stacking Columns of Face Data                         #
Face_Data_Out_0 = np.column_stack((fx,fy))              #
Face_Data       = np.column_stack((Face_Data_Out_0,fz)) #
#########################################################
#
################################
# Tetrahedron Center of Masses #
################################
# Get data size for range
data_size=np.shape(Face_Data)[0]
# Make an empty list
Center_mass_tetra = []
# Start Calculations
# 
# - Use Faces as the index !!
for ii in range(0,data_size):
#Debugg: ic(Face_Data[ii,0],Face_Data[ii,1],Face_Data[ii,2])
     Center_mass_calc_x = (Vert_Data[Face_Data[ii,0],0] + Vert_Data[Face_Data[ii,1],0] + Vert_Data[Face_Data[ii,2],0] + CM[0])/4
     Center_mass_calc_y = (Vert_Data[Face_Data[ii,0],1] + Vert_Data[Face_Data[ii,1],1] + Vert_Data[Face_Data[ii,2],1] + CM[1])/4
     Center_mass_calc_z = (Vert_Data[Face_Data[ii,0],2] + Vert_Data[Face_Data[ii,1],2] + Vert_Data[Face_Data[ii,2],2] + CM[2])/4
     Center_mass_calc   = np.array([Center_mass_calc_x,Center_mass_calc_y,Center_mass_calc_z])
     # Fill list
     Center_mass_tetra.append(Center_mass_calc)
#ic(Center_mass_tetra)
######################################
#
########################################
# Prompt user for scaling the asteroid #
########################################
Scaling_Prompt =f"""
{'-'*42}
|  Would you like this scaled to the approximated mean radius?
"""
print(Scaling_Prompt)
Scaling_Choice = input('| Please enter Y/N: ')
# Will the asteroid be scaled?
if Scaling_Choice == 'Y' or Scaling_Choice == 'y':
    # Ask user for correct mean radius
    Radius_input = float(input('| Please Enter the mean radius: '))
    # Calculate radius from OBJ file
    vec_x = Vert_Data[:,0] - CM[0]
    vec_y = Vert_Data[:,1] - CM[1]
    vec_z = Vert_Data[:,2] - CM[2]
    Radius_Calc = np.sqrt(vec_x**2 + vec_y**2 + vec_z**2)
    # Calculate mean raddius from OBJ file
    Mean_radius_calc = np.mean(Radius_Calc)
    # Calculate the proper scale 
    Scale = Radius_input/Mean_radius_calc
    # Check this produces the proper mean radius
    Mean_Radius_Scaled = Mean_radius_calc*Scale
    ic(Radius_Calc)
    ic(Mean_Radius_Scaled)
    # Print scale data is multipled by to the user 
    ic(Scale)
    # Scale Outputs
    Vert_Data_mesh = Vert_Data*Scale
    Output_Array_CM = np.array(Center_mass_tetra)*Scale
# Tell user this data is NOT to scale    
elif Scaling_Choice == 'N' or Scaling_Choice == 'n':
    Scaling_Disclaimer = f"""
{'-'*42}
|  You have selected NOT to scale the data
|    to the correct mean radius.
|
|   Disclaimer: The Center of Mass calculations
|                   are NOT to Scale!
{'-'*42}
"""
    print(Scaling_Disclaimer)
    Output_Array_CM = np.array(Center_mass_tetra)
# Input ERROR!!
else:
    Exit_Error_Message = f"""
{'-'*42}
| Error!! please use either Y or N (not case sensitive)
|         to select scaling
{'-'*42}
    """
    print(Exit_Error_Message)
    input('|press any key to exit... ')
    exit() 
#################################################
#
####################
# Text File output #
####################
# Save Data as .out
np.savetxt(Asteroid_file_in+".out", Output_Array_CM,delimiter=' ');
Data_message = f"""
{'-'*42}
| Data ready, See program directory
{'-'*42}
"""
print(Data_message)
###########################
#
########
# Plot #
########
figure = plt.figure()
axis   = figure.add_subplot(projection='3d')
#
# Plot it
xp = Output_Array_CM[:,0]
yp = Output_Array_CM[:,1]
zp = Output_Array_CM[:,2]
# Debugg
size = np.shape(xp)
ic(size)
#
axis.scatter3D(xp,yp,zp,
               marker='.',
               color='red')
#
plt.show()

