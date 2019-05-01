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
        self.coordinates = c_Coordinates() #Zestaw danych wejsciowych w postaci lokazliacji punktu (X,Y,Z) i jego orientacji w formie kwaternionu
        self.coordinate_system = np.zeros([4,4]) #Zawiera dane z pola coordinates przekształcone do postaci macierzowej
        self.checked = False                

    # Złożenie macierzy translacji i rotacji w jedną macierz definiującą dany układ współrzednych
    def get_coordinate_system(self):
        quaternion = self.get_quaternion_from_file()
        temp_matrix = quaternion.rotation_matrix
        for i in range(3):
           for j in range(3):
               if(i < 3) & (j < 3):
                   self.coordinate_system[i,j] = temp_matrix[i,j]

        self.coordinate_system[0,3] = self.coordinates.x
        self.coordinate_system[1,3] = self.coordinates.y
        self.coordinate_system[2,3] = self.coordinates.z
        self.coordinate_system[3,3] = 1.0

    #Generuje kwaternion opisujacy rotacje ukladu na podstawie danych odczytanych z pliku
    def get_quaternion_from_file(self):
        qt = pq.Quaternion(self.coordinates.scalar, self.coordinates.rotx, self.coordinates.roty, self.coordinates.rotz)
        return qt

    # Generuje kwaternion opisujący rotację układu w przestrzeni po wykonaniu przekształceń
    def get_quaternion_from_matrix(self):
        qt = pq.Quaternion(matrix = self.coordinate_system)
        self.coordinates.scalar = qt.w
        self.coordinates.rotx = qt.x
        self.coordinates.roty = qt.y
        self.coordinates.rotz = qt.z

    # Konwersja z radianów na stopnie 
    def rad2deg(self):
        for i in range(3):
            for j in range(3):
                if(i < 3) & (j < 3):
                    self.coordinate_system[i][j] = self.coordinate_system[i][j] * 180.0 / np.pi

     # Zaokrągla dane liczbowe do zadanej liczby miejsc po przecinku
    def round_floats(self, number_of_digits):
        self.coordinates.x = round(self.coordinates.x,number_of_digits)
        self.coordinates.y = round(self.coordinates.y,number_of_digits)
        self.coordinates.z = round(self.coordinates.z,number_of_digits)
        self.coordinates.scalar = round(self.coordinates.scalar,number_of_digits)
        self.coordinates.rotx = round(self.coordinates.rotx,number_of_digits)
        self.coordinates.roty = round(self.coordinates.roty,number_of_digits)
        self.coordinates.rotz = round(self.coordinates.rotz,number_of_digits)
    