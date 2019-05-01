import yaml


class c_Format(object):
    
    def __init__(self,record):
        self.id = str(record.id)
        self.name = str(record.name)
        self.master_id = str(record.master_id)
        self.inverted = str(record.inverted)
        self.location = "[ " + str(record.coordinates.x) + " " + str(record.coordinates.y) + " " + str(record.coordinates.z) + "]"
        self.orientation = "[ " + str(record.coordinates.scalar) + " " + str(record.coordinates.rotx) + " " + str(record.coordinates.roty) + " " + str(record.coordinates.rotz) + "]"   
    
    def __repr__(self):
        return "%s(id=%r, name=%r, master_id=%r, inverted=%r, location=%r, orientation=%r)" % (
            self.__class__.__name__, self.id, self.name, self.master_id, self.inverted, self.location, self.orientation)

