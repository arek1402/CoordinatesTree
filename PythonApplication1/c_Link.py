import numpy as np
import pyquaternion as pq
from c_Coordinates import *

class c_Link(object):

    # Konstruktor klasy
    def __init__(self):
        self.name = ""
        self.id = -1
        self.master_id = 0
        self.inverted = 0
        self.coordinates = c_Coordinates()
        self.rot_matrix = np.zeros([4,4])
        self.translation = np.zeros(3)
        self.coordinate_system = np.zeros([4,4])
        self.checked = False

    # Przepisanie danych odczytanych z pliku do macierzy translacji
    def get_translation_matrix(self):
        self.translation = np.array([self.coordinates.x, self.coordinates.y, self.coordinates.z])

    # Przepisanie kwaternionów odczytanych z pliku do macierzy rotacji
    def get_rotation_matrix(self):
        quaternion = pq.Quaternion(self.coordinates.scalar, self.coordinates.rotx, self.coordinates.roty, self.coordinates.rotz)
        self.rot_matrix = quaternion.rotation_matrix
        i=0
        j=0
        for i in range(3):
           for j in range(3):
               if(i < 3) & (j < 3):
                   self.coordinate_system[i,j] = self.rot_matrix[i,j]
                

    # Złożenie macierzy translacji i rotacji w jedną macierz definiującą dany układ współrzednych
    def get_coordinate_system(self):
        #self.coordinate_system = self.rot_matrix
        self.coordinate_system[0,3] = self.translation[0]
        self.coordinate_system[1,3] = self.translation[1]
        self.coordinate_system[2,3] = self.translation[2]
        self.coordinate_system[3,3] = 1.0
        #print(self.coordinate_system)

    # Pobiera informacje dotyczące translacji z przekształconego układu współrzednych
    def get_translation_params(self):
        self.coordinates.x = self.coordinate_system[0,3]
        self.coordinates.y = self.coordinate_system[1,3] 
        self.coordinates.z = self.coordinate_system[2,3] 

    # Generuje kwaternion opisujący rotację układu w przestrzeni po wykonaniu przekształceń
    def get_quaternion(self):
        qt = pq.Quaternion(matrix = self.coordinate_system)
        self.coordinates.scalar = qt.w
        self.coordinates.rotx = qt.x
        self.coordinates.roty = qt.y
        self.coordinates.rotz = qt.z

    # Konwersja ze stopni na radiany
    def rad2deg(self):
        for i in range(len(self.rot_matrix)):
            for j in range(len(self.rot_matrix[i])):
                self.rot_matrix[i][j] = self.rot_matrix[i][j] * 180.0 / np.pi




    