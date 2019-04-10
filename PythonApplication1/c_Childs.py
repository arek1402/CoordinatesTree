import numpy as np
from c_Link import *
from c_Coordinates import *
from f_Functions import *

class c_Childs(object):
    """description of class"""
    def __init__(self):
        id = -1
        link = c_Link()
        transformation_matrix = np.array([4,4])


    # Wyzancza macierz transformacji z układu nadrzędnego do układu współrzędnych potomka
    def get_transformation_matrix(self, trans_master, trans_child):
        self.transformation_matrix = np.matmul(trans_master, trans_child)


