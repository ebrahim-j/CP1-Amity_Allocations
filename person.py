""" Declaration of classes Person, Fellow, Staff """

class Person(object):
    """ class Person """


    def __init__(self, the_id, the_name):
        self.the_id = the_id
        self.the_name = the_name

    
class Fellow(Person):
    def __init__(self, the_id, the_name):
        super(Fellow, self).__init__(the_id, the_name)
        self.allocated = False
        self.accommodated = False


class Staff(Person):
    def __init__(self, the_id, the_name):
        super(Staff, self).__init__(the_id, the_name)
        self.allocated = False
