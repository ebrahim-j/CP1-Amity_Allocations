""" Functions consisted in class Amity """
from person import Person

class Amity(object):
    """ class Amity """
    def __init__(self):
        pass

    def reallocate_person(self, name_id, new_room_name):
        """ Reallocates a person with person_identifier to new_room_name """
        pass

    def load_people(self): #, fileobj
        """ Adds people to rooms from a txt file """
        #try except this to see if file exists
        # fileobj = open("filename.txt", "r")

        # if not fileobj.closed:
        #     print("file is already opened")
        # else:
        #     fileobj.read()
        #     for line in fileobj:
        #         read1line = line.split()
        #         if len(read1line) == 3:
        #             name = read1line[0]
        #             type_person = read1line[1]
        #             wants_accomodation = read1line[2]
        #             Person.add_person(name, type_person, wants_accomodation)
        #         else:
        #             name = read1line[0]
        #             type_person = read1line[1]
        #             Person.add_person(name, type_person)
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
