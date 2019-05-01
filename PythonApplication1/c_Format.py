class c_Format(object):
    
    def __init__(self):
        self.id = "-1"
        self.name = "empty_name"
        self.master_id = "-1"
        self.inverted = "-1"
        self.location = "[x y z]"
        self.orientation = "[scalar rotx roty rotz]"

    def fill_the_fields(self, record):
        self.id = str(record.id)
        self.name = str(record.name)
        self.master_id = str(record.master_id)
        self.inverted = str(record.inverted)
        self.location = "[ " + str(record.coordinates.x) + " " + str(record.coordinates.y) + " " + str(record.coordinates.z) + "]"
        self.orientation = "[ " + str(record.coordinates.scalar) + " " + str(record.coordinates.rotx) + " " + str(record.coordinates.roty) + " " + str(record.coordinates.rotz) + "]"
    """description of class"""


