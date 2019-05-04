import yaml
from c_Link import *

class c_Record(object):

    def __init__(self):
        self.id = ''
        self.name = ''
        self.master_id = ''
        self.inverted = ''
        self.position = ''
        self.orientation = ''

        #Tworzy zagnieżdzone listy zgodne z formatem YAML
    def prepare_data_to_save(self,data):
        self.id = str(data.id)
        self.name = data.name
        self.master_id = str(data.master_id)
        self.inverted = str(data.inverted)
        self.position = {'X': str(data.coordinates.x), 'Y': str(data.coordinates.y), 'Z': str(data.coordinates.z)}
        self.orientation = {'Scalar': str(data.coordinates.scalar), 'RotX': str(data.coordinates.rotx), 'RotY': str(data.coordinates.roty), 'RotZ': str(data.coordinates.rotz)}

        #Generuje rekord danych zapisywanych do pliku. Jeden rekord zawiera dane dotyczące jednego układu współrzędnych
    def generate_record_to_save(self):
        record = {'Link': {'ID': self.id, 'Name': self.name, 'Master_ID': self.master_id, 'Inverted': self.inverted, 'Position': self.position, 'Orientation': self.orientation}}
        return record



