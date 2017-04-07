""" Functions consisted in class Amity """
from person import Fellow, Staff
from rooms import Office, LivingSpace, Room
from random import randint, choice

class Amity(object):
    """ class Amity """
    def __init__(self):
        self.fellows = []
        self.staff = []
        self.offices = []
        self.l_spaces = []

    def randomly_allocate_office(self, person):
        self.rooms_with_space = []
        for room in self.offices:
            if Room.room_has_space(room):
                self.rooms_with_space.append(room)
        self.the_room = choice(self.rooms_with_space)
        self.the_room.current_occupants.append(person.the_name)
        person.allocated = True
        return self.the_room.room_name
    
    def randomly_allocate_ls(self, person):
        self.rooms_with_space = []
        for room in self.l_spaces:
            if room.room_has_space(room):
                self.rooms_with_space.append(room)
        self.the_room = choice(self.rooms_with_space)
        self.the_room.current_occupants.append(person.the_name)
        person.accomodation = True
        return self.the_room.room_name 

    def add_person(self, name, role, wants_accommodation='N'):
        #try for edge cases here
        self.identifier = randint(1, 9999) #query the db
        if role.lower() == "staff":
            wants_accommodation = "N"
            self.person = Staff(self.identifier, name)
            self.staff.append(self.person)
            #randomly_allocate_office(person) #allocated attribute becomes true, make it return an office
            print("Staff created")
        elif role.lower() == "fellow":
            if wants_accommodation.upper() == "N" or wants_accommodation.upper() == "NO": #what if wants_acc says something beside y or n?
                self.person = Fellow(self.identifier, name)
                self.fellows.append(self.person)
                #ramdomly_allocate_office(name)
                print("fellow1 has been added")
            elif wants_accommodation.upper() == "Y" or wants_accommodation.upper() == "YES":
                self.person = Fellow(self.identifier, name)
                self.fellows.append(self.person)
                #randomly_allocate_office(name)
                #randomly_allocate_ls(name)
                print("fellow2 has been added")
            else:
                print("I don't know whether you want accomodation or not. (Reply with Y or Yes, N or No) ")
        else:
            print("Person can either be Staff or Fellow")
            



    def create_room(self, prefix, name):
        """instantiates a living space or office based on prefix"""
        #check for edge cases here    

        if prefix.lower() == "office" or prefix.lower() == "o": #try regex
            self.room = Office(name)
            self.offices.append(self.room)
            print("We have successfully created a new office called: %s!", self.room.room_name.upper())
        elif prefix.lower() == "living space" or prefix.lower() == "livingspace" or prefix.lower() == "l" or prefix.lower() == "ls": #try regex
            self.room = LivingSpace(name)
            self.l_spaces.append(self.room)
            print("New living quarters ( %s ) successfully created!", self.room.upper())

    def reallocate_person(self, name_id, new_room_name):
        """ Reallocates a person with person_identifier to new_room_name """
        pass

    # def load_people(self): #, fileobj
    #     """ Adds people to rooms from a txt file """
    #     #try except this to see if file exists
    #     # if fileobj[-4:] != '.txt':
    #     #     print("System can only load people from a text file")

    #     fileobj = open("filename.txt", "r")

    #     if not fileobj.closed:
    #         print("file is already opened")
    #     else:
    #         fileobj.read()
    #         for line in fileobj:
    #             read1line = line.split()
    #             name = read1line[0]
    #             role = read1line[1]
    #             if len(read1line) == 3:

    #                 if role.upper() == "STAFF":
    #                     wants_accommodation = "N"
    #                 else:
    #                     wants_accommodation = read1line[2]
    #                 Person.add_person(name, role, wants_accommodation)
    #             else:
    #                 Person.add_person(name, role, wants_accommodation='N')

    def load_people(self):
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

#get clarity about if printing allocations/unallocated would require a kind of load state OR it's just the data while the program is running.
# OR loads data first whenever program runs