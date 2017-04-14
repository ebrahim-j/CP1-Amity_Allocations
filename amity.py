""" Functions consisted in class Amity """
from person import Fellow, Staff
from rooms import Office, LivingSpace, Room
from random import randint, choice
#correct for .lower() or likewise entries
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
        # if not name.isalpha() or not role.isalpha() or not wants_accommodation.isalpha():
        #     return "Please ensure you don't have digits in name, role or accommodation"
        if name.lower() in ("staff", "fellow"):
            return "Person cannot have name 'Staff' or 'Fellow'"
        identifier = 1 #randint(1, 9999) #query the db?
        if role.lower() == "staff":
            wants_accommodation = "N"
            person = Staff(identifier, name)
            self.staff.append(person)
            office_selected = Amity.randomly_allocate_office(self)
            if office_selected == False:
                return "Welcome %s, You will be allocated an office as soon as we have space" % person.the_name
            office_selected.current_occupants.append(person.the_name)
            person.allocated = office_selected.room_name
            print ( "(%s): %s has been allocated to %s" % (person.the_id, person.the_name, office_selected.room_name))

        elif role.lower() == "fellow":
            if wants_accommodation.upper() == "N" or wants_accommodation.upper() == "NO": #what if wants_acc says something beside y or n?
                person = Fellow(identifier, name)
                self.fellows.append(person)
                office_selected = Amity.randomly_allocate_office(self)
                if office_selected == False:
                    return "Welcome (%s) %s, You will be allocated an office as soon as we have space" %(person.the_id, person.the_name )
                office_selected.current_occupants.append(person.the_name)
                person.allocated = office_selected.room_name
                print ("(%s): %s has been allocated to %s" % (person.the_id, person.the_name, office_selected.room_name))
            elif wants_accommodation.upper() == "Y" or wants_accommodation.upper() == "YES":
                person = Fellow(identifier, name)
                self.fellows.append(person)
                office_selected = Amity.randomly_allocate_office(self)
                ls_selected = Amity.randomly_allocate_ls(self)
                if office_selected == False and ls_selected == False:
                    print("Welcome (%s) %s, You will be allocated an office and a Living Space as soon as we have space" % (person.the_id,person.the_name))
                elif office_selected == False and ls_selected != False:
                    ls_selected.current_occupants.append(person.the_name)
                    person.accommodated = ls_selected.room_name
                    print("Welcome (%s) %s, You will live in %s and will be allocated an office as soon as we have space" %(person.the_id, person.the_name, ls_selected.room_name))
                elif ls_selected == False and office_selected != False:
                    office_selected.current_occupants.append(person.the_name)
                    person.allocated = office_selected.room_name
                    print("Welcome (%s) %s, You have been allocated to %s. You will be assigned a living space as soon as we have room" %(person.the_id, person.the_name, office_selected.room_name))
                else:
                    office_selected.current_occupants.append(person.the_name)
                    person.allocated = office_selected.room_name
                    ls_selected.current_occupants.append(person.the_name)
                    person.accommodated = ls_selected.room_name
                    print ("(%s): %s has been appointed to %s and will live in %s" % (person.the_id, person.the_name, office_selected.room_name, ls_selected.room_name))
            else:
                print("I don't know whether you want accomodation or not. (Reply with Y or Yes, N or No) ")
        else:
            print("Person can either be Staff or Fellow")




    def create_room(self, prefix, name):
        """instantiates a living space or office based on prefix"""
        #check for edge cases here    
        #query the db to see if room already exists
        if not prefix.isalpha():
            return "Room type cannot be in digits"
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
                    #add to another's current occupants
                    for room in self.offices:
                        if individual.the_name in room.current_occupants:
                            room.current_occupants.remove(individual.the_name)
                    for room in self.offices:
                        if room.room_name == new_room_name and room.room_has_space():
                            room.current_occupants.append(individual.the_name)
                            individual.allocated = new_room_name
                    return "%s has been reallocated to %s" % (individual.the_name, new_room_name)
                elif not isinstance(individual, Staff) and new_room_name.lower() in [room.room_name.lower() for room in self.l_spaces]:
                    for room in self.l_spaces:
                        if individual.the_name in room.current_occupants:
                            room.current_occupants.remove(individual.the_name)
                    for room in self.l_spaces:
                        if room.room_name == new_room_name and room.room_has_space():
                            room.current_occupants.append(individual.the_name)
                            individual.accommodated = new_room_name
                    return "%s has been reallocated to %s" % (individual.the_name, new_room_name)
                elif isinstance(individual, Staff) and new_room_name.lower() in [room.room_name.lower() for room in self.l_spaces]:
                    return "Cannot allocate staff to a living Space"
                else:
                    return "This room does not exist. (Make sure you spell check your room names)"
            else:
                return "This person cannot be identified"

    def load_people(self, fileobj):
        """ Adds people to rooms from a txt file """
        #try except this to see if file exists
        # try:
        if fileobj[-4:] != '.txt':
            return "System can only load people from a text file"

        with open(fileobj, 'r') as my_file:
            info = my_file.readlines()
            for argument in info:
                argument = argument.split()
                name = str(argument[0]) + " " + str(argument[1])
                role = str(argument[2].strip())
                if len(argument) == 3:
                    wants_accommodation = "N"
                    print(self.add_person(name, role, wants_accommodation))
                else:
                    wants_accommodation = str(argument[3])
                    print(self.add_person(name, role, wants_accommodation))      
                # return "Information provided not complete"



        # except:
        #     return "File does not exist"


    def print_allocations(self):
        """ Prints a list of allocations.
        Specifying the optional -o option outputs the registered allocations to a txt file """

        if len(self.offices) == 0:
            print("NO offices added yet!")
        else:
            print ("OFFICES:")
            print ("="*8)
            for room in self.offices:
                print(room.room_name.upper())
                print("")
                print('-'*20)
                print("")
                print(', '.join(room.current_occupants))
                print("")
                print("")
        if len(self.l_spaces) == 0:
            print("NO living spaces added yet!")
        else:
            print ("LIVING SPACES:")
            print ("="*14)
            for room in self.l_spaces:
                print(room.room_name.upper())
                print("")
                print('-'*20)
                print("")
                print(', '.join(room.current_occupants))
                print("")


    def print_unallocated(self):
        """ Prints a list of unallocated people to the screen.
        Specifying the -o option here outputs the information to the txt file provided """
        unallocated = []
        everyone = self.fellows + self.staff #refactor to see if you can print which office is missing as well. Maybe 2 separate loops
        for one_person in everyone:
            if one_person.allocated == None:
                unallocated.append([one_person.the_id, one_person.the_name])
            elif not isinstance(one_person, Staff) and one_person.accommodated == None:
                unallocated.append([one_person.the_id, one_person.the_name])

        for person in unallocated:
            print("%s:- %s" % (person[0], person[1]))

    def print_room(self, room_name):
        """ Prints the names of all the people in room_name on the screen """
        all_rooms = self.offices + self.l_spaces
        try:
            for one_room in all_rooms:
                if room_name in [room.room_name for room in all_rooms] and room_name.lower() == one_room.room_name.lower():
                    print ("Occcupants in %s:" % one_room.room_name.upper())
                    print (", ".join(one_room.current_occupants))
        except:
            return "Room not found"


    def save_state(self):
        """ Persists all the data stored in the app to a SQLite database.
        Specifying the --db parameter explicitly stores the data in the
        sqlite_database specified """
        pass

    def load_state(self):
        """ Loads data from a database into the application """
        pass

amity = Amity()

amity.create_room("o", "oculus")
amity.create_room("l", "Homabay")
amity.create_room("l", "Surat")
amity.create_room("o", "Rome")
# amity.add_person("Faith", "fellow")
amity.add_person("Mulobi", "fellow", "Yes")
# amity.add_person("Alex", "staff", "Y")
# amity.add_person("Paul", "fellow", "Y")
# amity.add_person("Millicent", "staff", "N")
# amity.add_person("Ahmed", "fellow", "N")
# print(amity.load_people("text.txt"))
# amity.print_allocations()
amity.print_room("Surat")
amity.print_room("Homabay")

print("")
amity.print_unallocated()
print(amity.reallocate_person(11, "Surat"))

amity.print_room("Surat")
amity.print_room("Homabay")
# import pdb; pdb.set_trace()
