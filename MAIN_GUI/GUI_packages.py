##########################
# Capstone GUI Functions #
##########################
import numpy as np
from icecream import ic 
##############################
#
def READ_IN(Asteroid_Name):
    """_summary_

    Args:
        Astertoid_Name (_type_): _description_
    """
    #######################
    # Load data file      ###################################### 
    data = np.loadtxt(Asteroid_Name, delimiter=' ', dtype=str) #
    ############################################################
    Tetra_CM = data.astype(float)
    return Tetra_CM
