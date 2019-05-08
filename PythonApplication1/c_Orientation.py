class c_Orientation(object):

    def __init__(self):
        self.scalar = 0.0
        self.rotx = 0.0
        self.roty = 0.0
        self.rotz = 0.0

    def assingn_data(self,data):
        self.scalar = data[0]
        self.rotx = data[1]
        self.roty = data[2]
        self.rotz = data[3]

