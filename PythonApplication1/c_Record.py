import yaml

class c_Record(object):

    def __init__(self):
        self.id = ''
        self.name = ''
        self.master_id = ''
        self.inverted = ''
        self.position = ''
        self.orientation = ''

    def prepare_data_to_save(self,data):
        self.id = data.id
        self.name = data.name
        self.master_id = data.master_id
        self.inverted = data.inverted
        self.position = {'X': data.coordinates.x, 'Y': data.coordinates.y, 'Z': data.coordinates.z}
        self.orientation = {'Scalar': str(data.coordinates.scalar), 'RotX': str(data.coordinates.rotx), 'RotY': str(data.coordinates.roty), 'RotZ': str(data.coordinates.rotz)}
    
    def generate_record_to_save(self):
        record = {'Link': {'ID': self.id, 'Name': self.name, 'Master_ID': self.master_id, 'Inverted': self.inverted, 'Position': self.position, 'Orientation': self.orientation}}
        return record



