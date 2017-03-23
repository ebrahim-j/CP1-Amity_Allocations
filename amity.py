""" Functions consisted in class Amity """

class Amity(object):
    """ class Amity """
    def __init__(self):
        pass

    def reallocate_person(self, name_id, new_room_name):
        """ Reallocates a person with person_identifier to new_room_name """
        pass

    def load_people(self):
        """ Adds people to rooms from a txt file """
        pass

    def print_allocations(self):
        """ Prints a list of allocations.
        Specifying the optional -o option outputs the registered allocations to a txt file """
        pass

    def print_unallocated(self):
        """ Prints a list of unallocated people to the screen.
        Specifying the -o option here outputs the information to the txt file provided """
        pass

    def print_room(self, room_name):
        """ Prints the names of all the people in room_name on the screen """
        pass

    def save_state(self):
        """ Persists all the data stored in the app to a SQLite database.
        Specifying the --db parameter explicitly stores the data in the
        sqlite_database specified """
        pass

    def load_state(self):
        """ Loads data from a database into the application """
        pass
