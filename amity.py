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

    def randomly_allocate_office(self):
        rooms_with_space = []
        for room in self.offices:
            if room.room_has_space():
                rooms_with_space.append(room)
        if len(rooms_with_space) == 0:
            return False
        selected_room = choice(rooms_with_space)
        return selected_room

    
    def randomly_allocate_ls(self):
        rooms_with_space = []
        for room in self.l_spaces:
            if room.room_has_space() == True:
                rooms_with_space.append(room)
        if len(rooms_with_space) == 0:
            return False
        selected_room = choice(rooms_with_space)
        return selected_room

    
    def add_person(self, name, role, wants_accommodation='N'):
        #try for edge cases here
        identifier = randint(1, 9999) #query the db?
        if role.lower() == "staff":
            wants_accommodation = "N"
            person = Staff(identifier, name)
            self.staff.append(person)
            room_selected = Amity.randomly_allocate_office(self)
            if room_selected == False:
                return "Welcome %s, You will be allocated an office as soon as we have space" %person.the_name
            room_selected.current_occupants.append(person.the_name)
            person.allocated = room_selected.room_name
            print ( "(%s): %s has been allocated to %s" % (person.the_id, person.the_name, room_selected.room_name))

        elif role.lower() == "fellow":
            if wants_accommodation.upper() == "N" or wants_accommodation.upper() == "NO": #what if wants_acc says something beside y or n?
                person = Fellow(identifier, name)
                self.fellows.append(person)
                room_selected = Amity.randomly_allocate_office(self)
                room_selected.current_occupants.append(person.the_name)
                person.allocated = room_selected.room_name
                print ( "(%s): %s has been allocated to %s" % (person.the_id, person.the_name, room_selected.room_name))
            elif wants_accommodation.upper() == "Y" or wants_accommodation.upper() == "YES":
                person = Fellow(identifier, name)
                self.fellows.append(person)
                room_selected = Amity.randomly_allocate_office(self)
                room_selected.current_occupants.append(person.the_name)
                person.allocated = room_selected.room_name
                ls_selected = Amity.randomly_allocate_ls(self)
                ls_selected.current_occupants.append(person.the_name)
                person.accommodated = ls_selected.room_name
                print ("(%s): %s has been appointed to %s and will live in %s" % (person.the_id, person.the_name, room_selected.room_name, ls_selected.room_name))
            else:
                print("I don't know whether you want accomodation or not. (Reply with Y or Yes, N or No) ")
        else:
            print("Person can either be Staff or Fellow")
            



    def create_room(self, prefix, name):
        """instantiates a living space or office based on prefix"""
        #check for edge cases here    

        if prefix.lower() == "office" or prefix.lower() == "o": #try regex
            room = Office(name)
            self.offices.append(room)
            result = "We have successfully created a new office called: %s" % room.room_name.upper()
            return result
        elif prefix.lower() == "living space" or prefix.lower() == "livingspace" or prefix.lower() == "l" or prefix.lower() == "ls": #try regex
            room = LivingSpace(name)
            self.l_spaces.append(room)
            result = "New living quarters ( %s ) successfully created!" % room.room_name.upper()
            return result
        else:
            return "This"

    def reallocate_person(self, name_id, new_room_name):
        """ Reallocates a person with person_identifier to new_room_name """
        employees = self.fellows + self.staff

        for individual in employees:
            if individual.the_id == name_id:
                if new_room_name.lower() in [room.room_name.lower() for room in self.offices]: #check for when person is alloccated to same room
                    #what if staff is tried to be allocated to living space?
                    individual.allocated = new_room_name
                    return "%s has been reallocated to %s" % (individual.the_name, new_room_name)
                elif new_room_name.lower() in [room.room_name.lower() for room in self.l_spaces]:
                    individual.accommodated = new_room_name
                    return "%s has been reallocated to %s" % (individual.the_name, new_room_name)
                else:
                    return "This room does not exist. (Make sure you spell check your room names)"
            else:
                return "This person cannot be identified"

    def load_people(self, fileobj): 
        """ Adds people to rooms from a txt file """
        #try except this to see if file exists
        if fileobj[-4:] != '.txt':
            return "System can only load people from a text file"

        fileobj = open("filename.txt", "r")

        if not fileobj.closed:
            print("file is already opened")
        else:
            fileobj.read()
            for line in fileobj:
                read1line = line.split()
                name = read1line[0]
                role = read1line[1]
                if len(read1line) == 3:

                    if role.upper() == "STAFF":
                        wants_accommodation = "N"
                    else:
                        wants_accommodation = read1line[2]
                    Person.add_person(name, role, wants_accommodation)
                else:
                    Person.add_person(name, role, wants_accommodation='N')

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

amity = Amity()
amity.create_room("o", "oculus")
amity.create_room("l", "Homabay")
amity.add_person("Faith", "fellow")
amity.add_person("Tina", "staff")
amity.add_person("Mulobi", "fellow", "Yes")
amity.add_person("Alex", "staff", "Y")
