import numpy as np
import pyquaternion as pq
from c_Position import *
from c_Orientation import *

class c_Link(object):

    # Konstruktor klasy
    def __init__(self):
        self.name = ""
        self.id = -1
        self.master_id = 0
        self.inverted = 0
        self.position = c_Position() #Zestaw danych wejsciowych w postaci lokazliacji punktu (X,Y,Z) i jego orientacji w formie kwaternionu
        self.orientation = c_Orientation() #Zestaw danych wejsciowych w postaci jego orientacji w formie kwaternionu
        self.coordinate_system = np.zeros([4,4]) #Zawiera dane z pola coordinates przekształcone do postaci macierzowej
        self.checked = False                
    
    # Nadawanie nowego ID
    def set_id(self, new_id):
        self.id = new_id

    # Złożenie macierzy translacji i rotacji w jedną macierz definiującą dany układ współrzednych
    def get_coordinate_system(self):
        quaternion = self.get_quaternion_from_file()
        temp_matrix = quaternion.rotation_matrix
        for i in range(3):
           for j in range(3):
               if(i < 3) & (j < 3):
                   self.coordinate_system[i,j] = temp_matrix[i,j]

        self.coordinate_system[0,3] = self.position.x
        self.coordinate_system[1,3] = self.position.y
        self.coordinate_system[2,3] = self.position.z
        self.coordinate_system[3,3] = 1.0

    #Generuje kwaternion opisujacy rotacje ukladu na podstawie danych odczytanych z pliku
    def get_quaternion_from_file(self):
        qt = pq.Quaternion(self.orientation.scalar, self.orientation.rotx, self.orientation.roty, self.orientation.rotz)
        return qt

    #Wyciąga położenie układu z macierzy przekształceń
    def get_translation_from_matrix(self):
        self.position.x = self.coordinate_system[0,3]
        self.position.y = self.coordinate_system[1,3]
        self.position.z = self.coordinate_system[2,3]

    # Generuje kwaternion opisujący rotację układu w przestrzeni po wykonaniu przekształceń
    def get_quaternion_from_matrix(self):
        qt = pq.Quaternion(matrix = self.coordinate_system)
        self.orientation.scalar = qt.w
        self.orientation.rotx = qt.x
        self.orientation.roty = qt.y
        self.orientation.rotz = qt.z

    # Konwersja z radianów na stopnie 
    def rad2deg(self):
        for i in range(3):
            for j in range(3):
                if(i < 3) & (j < 3):
                    self.coordinate_system[i][j] = self.coordinate_system[i][j] * 180.0 / np.pi

     # Zaokrągla dane liczbowe do zadanej liczby miejsc po przecinku
    def round_floats(self, number_of_digits):
        self.position.x = round(self.position.x,number_of_digits)
        self.position.y = round(self.position.y,number_of_digits)
        self.position.z = round(self.position.z,number_of_digits)
        self.orientation.scalar = round(self.orientation.scalar,number_of_digits)
        self.orientation.rotx = round(self.orientation.rotx,number_of_digits)
        self.orientation.roty = round(self.orientation.roty,number_of_digits)
        self.orientation.rotz = round(self.orientation.rotz,number_of_digits)
    
        #Przekształca pozycje lub orientacje do postaci listy na potrzeby zapisu do pliku
    def return_list(self,option):
        if(option == 1):
            result = np.array([self.position.x, self.position.y, self.position.z])
        elif(option == 2):
            result = np.array([self.orientation.scalar, self.orientation.rotx, self.orientation.roty, self.orientation.rotz])
        return result.tolist()