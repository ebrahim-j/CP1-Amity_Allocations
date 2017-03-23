""" Declaration of classes Person, Fellow, Staff """

class Person(object):
    """ class Person """


    def __init__(self, identifier=2, name=""): #, name, wants_accommodation="N"
        # self.wants_accommodation = wants_accommodation
        self.identifier = identifier
        self.name = name


    def add_person(self, name, type_person, wants_accommodation):
        pass


class Fellow(Person):
    def __init__(self):
        pass



class Staff(Person):
    def __init__(self):
        pass
