######################
# Apophis Recreation #
#######################
import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
#
###############
# User Inputs #
###############################################################
# Ask for Desired File Name                                   #
Asteroid_file_in = input('|Please input desired file name: ') #
# Add .obj extension to file name                             #
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
####################
# Text File output #
####################
# Save Data as .txt
np.savetxt(Asteroid_file_in+".out",Center_mass_tetra,delimiter=' ');
Data_message = f"""
{'-'*42}
| Data ready, See program directory
{'-'*42}
"""
print(Data_message)
###########################
########
# Plot #
########
figure = plt.figure()
axis   = figure.add_subplot(projection='3d')
#
# Plot it
arr = np.array(Center_mass_tetra)
xp = arr[:,0]
yp = arr[:,1]
zp = arr[:,2]
# Debugg
size = np.shape(xp)
ic(size)
#
axis.scatter3D(xp,yp,zp,
               marker='.',
               color='red')
#
plt.show()

