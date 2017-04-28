""" Declaration of classes; Room, Office, LivingSpace """
class Room(object):
    """ class Room """

    def __init__(self, room_name):
        self.room_name = room_name

class Office(Room):
    """ class Office inherits from class Room """
    def __init__(self, room_name):
        super(Office, self).__init__(room_name)
        self.current_occupants = []
        self.max_capacity = 6
        self.room_type = "OFFICE"

    def __str__(self):
        return "{}".format(self.room_name)

    def room_has_space(self):
        """ Checks a room to see whether it has space or not"""
        if len(self.current_occupants) < self.max_capacity:
            return True
        else:
            return False

class LivingSpace(Room):
    """ class LivingSpace inherits from class Room """
    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name)
        self.current_occupants = []
        self.max_capacity = 4
        self.room_type = "LIVING"


    def __str__(self):
        return "{}".format(self.room_name)

    def room_has_space(self):
        """ Checks a room to see whether it has space or not"""
        if len(self.current_occupants) < self.max_capacity:
            return True
        else:
            return False
