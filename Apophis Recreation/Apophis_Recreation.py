######################
# Apophis Recreation #
#######################
import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
#
#
Asteroid_file = ('Apophis.obj')
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
# - CM Apophis
CM = np.array([-0.002150,-0.001070,-0.000308])
# Get data size for range
data_size=np.shape(Face_Data)[0]
# Make an empty list
Center_mass_tetra = []
# Start Calculations
# 
# - Use Faces as the index !!
for ii in range(0,data_size):
     # ic(Vert_Data[Face_Data[ii,0],0],Vert_Data[Face_Data[ii,1],0],Vert_Data[Face_Data[ii,2],0])
     Center_mass_calc_x = (Vert_Data[Face_Data[ii,0],0] + Vert_Data[Face_Data[ii,1],0] + Vert_Data[Face_Data[ii,2],0] + CM[0])/4
     Center_mass_calc_y = (Vert_Data[Face_Data[ii,0],1] + Vert_Data[Face_Data[ii,1],1] + Vert_Data[Face_Data[ii,2],1] + CM[1])/4
     Center_mass_calc_z = (Vert_Data[Face_Data[ii,0],2] + Vert_Data[Face_Data[ii,1],2] + Vert_Data[Face_Data[ii,2],2] + CM[2])/4
     Center_mass_calc   = np.array([Center_mass_calc_x,Center_mass_calc_y,Center_mass_calc_z])
     # Fill list
     Center_mass_tetra.append(Center_mass_calc)
#ic(Center_mass_tetra)
#
##################
# Scaling Radius #
######################
Radius_input = float(input('Please Enter the mean radius: '))
#
ic(Vert_Data.max())
#
vec_x = Vert_Data[:,0] - CM[0]
vec_y = Vert_Data[:,1] - CM[1]
vec_z = Vert_Data[:,2] - CM[2]
#
Radius_initial_Calc = np.sqrt(vec_x**2 + vec_y**2 + vec_z**2)
# Conversion test
mean_radius = np.mean(Radius_initial_Calc)
#
Scale = Radius_input/mean_radius
#Scale = 0.285
mean_radius = mean_radius*Scale
#
ic(Scale)
#
Vert_Data_mesh = Vert_Data*Scale
# Output
ic(mean_radius)
arr = np.array(Center_mass_tetra)*Scale
'''
# Save Data 
np.savetxt("Radius.out",Radius,delimiter=' ');
Data_message = f"""
{'-'*42}
| Data ready, See program directory
{'-'*42}
"""
print(Data_message)
'''
########
# Plot #
########

##:)                                                 
# Let's put a Happy little Asteroid right in there        
Asteroid_Mesh = Poly3DCollection([Vert_Data_mesh[ii] for ii in Face_Data], 
                          edgecolor='#1A85FF',
                          facecolors="white",
                          linewidth=0.1,
                          alpha=0.0)
######################################

figure = plt.figure()
axis   = figure.add_subplot(projection='3d')
#
# Plot it
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
#axis.add_collection3d(Asteroid_Mesh)                #
# Set Asteroid Aspect Ratio         #################
axis.set_box_aspect(                                     #
    [np.ptp(coord) for coord in [xp, yp, zp]]) #
axis.set_xlabel('x (km)')
axis.set_ylabel('y (km)')
axis.set_zlabel('z (km)')
plt.show()
