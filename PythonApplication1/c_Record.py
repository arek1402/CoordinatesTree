import yaml
from c_Link import *

class c_Record(object):

    def __init__(self):
        self.name = ''
        self.master = ''
        self.inverted = ''
        self.position = ''
        self.orientation = ''

        #Tworzy zagnieżdzone listy zgodne z formatem YAML
    def prepare_data_to_save(self,data):
        self.name = str(data.name)
        self.master = str(data.master)
        self.inverted = int(data.inverted)
        self.position = [ float(data.position.x), float(data.position.y), float(data.position.z) ]
        self.orientation = [float(data.orientation.scalar), float(data.orientation.rotx), float(data.orientation.roty), float(data.orientation.rotz)]

        #Generuje rekord danych zapisywanych do pliku. Jeden rekord zawiera dane dotyczące jednego układu współrzędnych
    def generate_record_to_save(self,id):
        record = {'Link'+str(id): { 'Name': self.name, 'Master': self.master, 'Inverted': self.inverted, 'Position': self.position, 'Orientation': self.orientation}}
        return record



