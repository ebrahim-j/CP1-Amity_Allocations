""" Declaration of classes; Room, Office, LivingSpace """
class Room(object):
    """ class Room """

    def __init__(self, room_name): 
        self.room_name = room_name


    def room_has_space(self, obj_ref):
        if self.obj_ref.max_capacity > len(self.obj_ref.current_occupants):
            return True
        else:
            return False

class Office(Room):
    """ class Office inherits from class Room """
    def __init__(self, room_name):
        super(Office, self).__init__(room_name)
        self.current_occupants = []
        self.max_capacity = 6



class LivingSpace(Room):
    """ class LivingSpace inherits from class Room """
    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name)
        self.current_occupants = []
        self.max_capacity = 4
        
