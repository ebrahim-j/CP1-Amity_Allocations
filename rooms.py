""" Declaration of classes; Room, Office, LivingSpace """
class Room(object):
    """ class Room """

    def __init__(self, name='', max_capacity=0, current_occupants=[]): 
        self.name = name
        self.max_capacity = max_capacity
        self.current_occupants = current_occupants

    def create_room(self, prefix, name):

        #instantiates a living space or office based on prefix
        return ""


class Office(Room):
    """ class Office inherits from class Room """
    def __init__(self):
        pass



class LivingSpace(Room):
    """ class LivingSpace inherits from class Room """
    def __init__(self):
        pass
