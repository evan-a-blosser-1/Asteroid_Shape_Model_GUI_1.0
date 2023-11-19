##########################
# Capstone GUI Functions #
##########################
import numpy as np
from icecream import ic 
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
##############################
#
def READ_IN(Asteroid_Name):
    """_summary_

    Args:
        Asteroid_Name (.out file): This is the output file from 
                                    Asteroid_CM.py

    Returns:
        Array: The x-y-z points of each Center of Mass for 
                asteroid tetrahedrons 
    """
    #######################
    # Load data file      ###################################### 
    data = np.loadtxt(Asteroid_Name, delimiter=' ', dtype=str) #
    ############################################################
    Tetra_CM = data.astype(float)
    return Tetra_CM


def OBJ_READ_IN(Asteroid_Name,scale):
    """ This reads in .obj files and creates the face mesh
     That is used for plotting around the Center of Masses
     
    Args:
        Asteroid_Name (.obj file):  Asteroid Shape model File
    
    Returns:
        Mesh: Asteroid face mesh 
    """
    #######################
    # Load data file      ###################################### 
    data = np.loadtxt(Asteroid_Name, delimiter=' ', dtype=str) #
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
    Vert_Data_mesh = Vert_Data*scale
    ##:)                                                 
    # Let's put a Happy little Asteroid right in there        
    Asteroid_Mesh = Poly3DCollection([Vert_Data_mesh[ii] for ii in Face_Data], 
                            edgecolor='#FFC107',
                            facecolors="white",
                            linewidth=0.1,
                            alpha=0.0)
    ######################################
    return Asteroid_Mesh

