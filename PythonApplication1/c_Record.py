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
        self.id = int(data.id)
        self.name = str(data.name)
        self.master_id = str(data.master_id)
        self.inverted = int(data.inverted)
        self.position = {'X': float(data.position.x), 'Y': float(data.position.y), 'Z': float(data.position.z)}
        self.orientation = {'Scalar': float(data.orientation.scalar), 'RotX': float(data.orientation.rotx), 'RotY': float(data.orientation.roty), 'RotZ': float(data.orientation.rotz)}

        #Generuje rekord danych zapisywanych do pliku. Jeden rekord zawiera dane dotyczące jednego układu współrzędnych
    def generate_record_to_save(self,id):
        record = {'Link'+str(id): {'ID': self.id, 'Name': self.name, 'Master_ID': self.master_id, 'Inverted': self.inverted, 'Position': self.position, 'Orientation': self.orientation}}
        return record



