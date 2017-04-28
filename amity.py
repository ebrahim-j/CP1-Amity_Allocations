""" Functions consisted in class Amity """
import os
from random import randint, choice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from termcolor import colored, cprint
from models.person import Fellow, Staff
from models.rooms import (Office, LivingSpace)
from models.dbModels import (RoomModel, PersonModel, Base)


class Amity(object):
    """ class Amity """

    def __init__(self):
        self.fellows = []
        self.staff = []
        self.offices = []
        self.l_spaces = []

    def randomly_allocate_office(self):
        """ Randomly allocates an office to a fellow/staff """
        rooms_with_space = []
        for room in self.offices:
            if room.room_has_space():
                rooms_with_space.append(room)
        if len(rooms_with_space) == 0:
            return False
        selected_room = choice(rooms_with_space)
        return selected_room

    def randomly_allocate_ls(self):
        """Randomly allocates a living space to a fellow"""
        rooms_with_space = []
        for room in self.l_spaces:
            if room.room_has_space() == True:
                rooms_with_space.append(room)
        if len(rooms_with_space) == 0:
            return False
        selected_room = choice(rooms_with_space)
        return selected_room

    def add_person(self, firstname, lastname, role, wants_accommodation='N'):
        """ Adds a staff/fellow to Amity and randomly allocates and office and/or living space"""
        all_people = self.fellows + self.staff
        identifier = randint(1, 9999)
        name = firstname + " " + lastname
        name = name.upper()
        output = ""
        if identifier in [person.the_id for person in all_people]:
            return colored("Duplicate ID generated. Please try again", "red")
        if role.lower() == "staff":
            if wants_accommodation is None:
                wants_accommodation = "N"
            if wants_accommodation.lower() not in ("n", "no"):
                output = colored(". Staff cannot be allocated a living space", "yellow")
            person = Staff(identifier, name)
            self.staff.append(person)
            office_selected = Amity.randomly_allocate_office(self)
            if office_selected is False:
                return colored("(%s) %s has been added and will be allocated an office as soon as we have space"%(person.the_id, person.the_name), "green") + output
            office_selected.current_occupants.append(person.the_name)
            person.allocated = office_selected.room_name
            return colored("(%s): %s has been allocated to the office %s" %
                           (person.the_id, person.the_name, office_selected.room_name), "cyan") \
                           + output
        elif role.lower() == "fellow":
            if wants_accommodation is None:
                wants_accommodation = "N"
            if wants_accommodation.upper() == "N" or wants_accommodation.upper() == "NO":
                person = Fellow(identifier, name)
                self.fellows.append(person)
                office_selected = Amity.randomly_allocate_office(self)
                if office_selected is False:
                    return colored("(%s) %s has been added and will be allocated an office as soon as we have space" % (person.the_id, person.the_name), "green")
                office_selected.current_occupants.append(person.the_name)
                person.allocated = office_selected.room_name
                return colored("(%s): %s has been allocated to %s" % (
                    person.the_id, person.the_name, office_selected.room_name), "cyan")
            elif wants_accommodation.upper() == "Y" or wants_accommodation.upper() == "YES":
                person = Fellow(identifier, name)
                self.fellows.append(person)
                office_selected = Amity.randomly_allocate_office(self)
                ls_selected = Amity.randomly_allocate_ls(self)
                if office_selected is False and ls_selected is False:
                    return colored("(%s) %s has been added and will be allocated an office and a Living Space as soon as we have space" % (
                         person.the_id, person.the_name), "green")
                elif office_selected is False and ls_selected != False:
                    ls_selected.current_occupants.append(person.the_name)
                    person.accommodated = ls_selected.room_name
                    return colored("(%s) %s will live in %s and will be allocated an office as soon as we have space" % (
                         person.the_id, person.the_name, ls_selected.room_name), "yellow")
                elif ls_selected is False and office_selected != False:
                    office_selected.current_occupants.append(person.the_name)
                    person.allocated = office_selected.room_name
                    return colored("(%s) %s has been allocated to %s. You will be assigned a living space as soon as we have room" % (
                         person.the_id, person.the_name, office_selected.room_name), "yellow")
                else:
                    office_selected.current_occupants.append(person.the_name)
                    person.allocated = office_selected.room_name
                    ls_selected.current_occupants.append(person.the_name)
                    person.accommodated = ls_selected.room_name
                    return colored("(%s): %s has been appointed to %s and will live in %s" %
                                   (person.the_id, person.the_name.upper(), \
                     office_selected.room_name.upper(), ls_selected.room_name.upper()), "cyan")
            else:
                return colored("I don't know whether you want accomodation or not. (Reply with Y or Yes, N or No) ", "red")
        else:
            return colored("Person can either be Staff or Fellow", "red")

    def get_everyone(self):
        """ Prints all the people in Amity on the screen"""
        everyone = self.fellows + self.staff

        if len(everyone) == 0:
            return colored("Nobody in Amity! :'(", "red")
        response = ""
        for guy in everyone:
            if isinstance(guy, Fellow):
                typeguy = "Fellow"
            else:
                typeguy = "Staff"
            response += "{} | {} | {}".format(guy.the_id, guy.the_name, typeguy) + "\n\n"
        return colored(response, "blue")


    def create_room(self, prefix, name):
        """instantiates a living space or office based on prefix"""
        all_rooms = self.offices + self.l_spaces
        if not name.isalpha():
            return colored("Room cannot have digits", "red")
        if not prefix.isalpha():
            return colored("Room type cannot be in digits", "red")
        name = name.upper()
        if prefix.lower() == "office" or prefix.lower() == "o":
            if name.upper() in [room.room_name.upper() for room in all_rooms]:
                return colored("Room name: %s already exists" % name, "red")
            room = Office(name)
            self.offices.append(room)
            result = "We have successfully created a new office called: %s" % room.room_name.upper()
            return colored(result, "cyan")
        elif prefix.lower() == "living space" or prefix.lower() == "livingspace"\
         or prefix.lower() == "l" or prefix.lower() == "ls":
            if name.upper() in [room.room_name.upper() for room in all_rooms]:
                return colored("Room name: %s already exists"%name, "red")
            room = LivingSpace(name)
            self.l_spaces.append(room)
            result = "New living quarters ( %s ) successfully created!" % room.room_name.upper(
            )
            return colored(result, "cyan")
        else:
            return colored("Room type: '%s' not recognized"%prefix, "red")


    def reallocate_person(self, person_id, new_room_name):
        """ Reallocates a person with person_identifier to new_room_name """
        employees = self.fellows + self.staff
        all_rooms = self.offices + self.l_spaces
        new_room_name = new_room_name.upper()

        for individual in employees:
            if individual.the_id == person_id:

                if new_room_name.upper() not in [room.room_name for room in all_rooms]:
                    return colored("This room does not exist. (Make sure you spell check your room names)", "red")
                if new_room_name.upper() == individual.allocated:
                    return colored("%s already in %s" %
                                   (individual.the_name, new_room_name), "yellow")
                elif new_room_name.upper() in [room.room_name for room in self.offices]:
                    for room in self.offices:
                        if room.room_name == new_room_name and not room.room_has_space():
                            return colored("Sorry, room is full", "green")
                    for room in self.offices:
                        if individual.the_name in room.current_occupants:
                            room.current_occupants.remove(
                                individual.the_name)
                    for room in self.offices:
                        if room.room_name == new_room_name and room.room_has_space():
                            room.current_occupants.append(
                                individual.the_name)
                        individual.allocated = new_room_name
                    return colored("%s has been reallocated to %s" %
                                   (individual.the_name, new_room_name), "cyan")
                elif not isinstance(individual, Staff) and new_room_name.lower()\
                 in [room.room_name.lower() for room in self.l_spaces]:
                    if new_room_name.upper() == individual.accommodated:
                        return colored("%s already in %s" %
                                       (individual.the_name, new_room_name), "yellow")
                    for room in self.l_spaces:
                        if room.room_name == new_room_name and not room.room_has_space():
                            return colored("Sorry, room is full", "green")
                    for room in self.l_spaces:
                        if individual.the_name in room.current_occupants:
                            room.current_occupants.remove(
                                individual.the_name)
                    for room in self.l_spaces:
                        if room.room_name == new_room_name and room.room_has_space():
                            room.current_occupants.append(
                                individual.the_name)
                        individual.accommodated = new_room_name
                    return colored("%s has been reallocated to %s" %
                                   (individual.the_name, new_room_name), "cyan")
                elif isinstance(individual, Staff) and new_room_name.lower() in [
                        room.room_name.lower() for room in self.l_spaces]:
                    return colored("Cannot allocate staff to a living Space", "red")

        return colored("This person cannot be identified", "red")


    def load_people(self, filename=None):
        """ Adds people to rooms from a txt file """
        if filename is None:
            filename = "text.txt"
        else:
            if filename[-4:] != ".txt":
                filename += ".txt"

        scriptpath = os.path.dirname(__file__)
        file_path = os.path.join(scriptpath, filename)

        try:
            with open(file_path, 'r') as my_file:
                info = my_file.readlines()
                if len(info) == 0:
                    return colored("File is empty", "yellow")
                for argument in info:
                    argument = argument.split()
                    firstname = str(argument[0].strip())
                    lastname = str(argument[1].strip())
                    role = str(argument[2].strip())
                    if len(argument) == 3:
                        wants_accommodation = "N"
                        self.add_person(firstname, lastname, role, wants_accommodation)
                    elif len(argument) == 4:
                        wants_accommodation = str(argument[3])
                        self.add_person(firstname, lastname, role, wants_accommodation)
                    else:
                        return colored("Inaccurate information. Double check your file", "red")
                return colored("File loaded successfully", "cyan")
        except:
            return colored("File does not exist", "red")


    def print_allocations(self, filename=None):
        """ Prints a list of allocations.
        Specifying the optional -o option outputs the registered allocations to a txt file """
        output = ""
        if len(self.offices) == 0:
            output = "NO offices added yet!\n"
        else:
            output = "OFFICES:\n" + ("=" * 8 + "\n")
            for room in self.offices:
                output += room.room_name.upper() + "\n" + ("-" * 50 + "\n")
                output += ", ".join(room.current_occupants) + "\n\n"
        if len(self.l_spaces) == 0:
            output += "NO living spaces added yet!"
        else:
            output += "LIVING SPACES:\n" + ("=" * 14 + "\n")
            for room in self.l_spaces:
                output += room.room_name.upper() + "\n" + ("-" * 50 + "\n")
                output += ", ".join(room.current_occupants) + "\n\n"

        if filename is None:
            return colored(output, "blue")
        else:
            if filename[-4:] != ".txt":
                filename += ".txt"
            with open(filename, 'w+') as my_file:
                my_file.write(output)
            return colored("Data has been successfully saved to {}".format(filename), "cyan")


    def print_unallocated(self, filename=None):
        """ Prints a list of unallocated people to the screen.
        Specifying the -o option here outputs the information to the txt file provided """
        unallocated = []
        everyone = self.fellows + self.staff
        for one_person in everyone:
            if isinstance(one_person, Staff):
                type_person = "Staff"
            else:
                type_person = "Fellow"
            if one_person.allocated is None and not isinstance(one_person, Staff) and\
             one_person.accommodated is None:
                unallocated.append([one_person.the_id, one_person.the_name, type_person,\
                 "Office", "Living Space"])
            elif one_person.allocated is None:
                unallocated.append([one_person.the_id, one_person.the_name, type_person, "Office"])
            elif not isinstance(one_person, Staff) and one_person.accommodated is None:
                unallocated.append([one_person.the_id, one_person.the_name, type_person,\
                 "Living Space"])

        if len(unallocated) == 0:
            return colored("This list is empty", "yellow")

        output = "The following people are unallocated: \n"
        for person in unallocated:
            if len(person) == 5:
                output += "%s:- %s (%s) ---> Not allocated with: %s and %s\n" %\
                (person[0], person[1], person[2], person[3], person[4])
            else:
                output += "%s:- %s (%s) ---> Not allocated with: %s\n" %\
                (person[0], person[1], person[2], person[3])

        if filename is None:
            return colored(output, "blue")
        else:
            if filename[-4:] != ".txt":
                filename += ".txt"
            with open(filename, 'w+') as my_file:
                my_file.write(output)
            return colored("Data has been successfully saved to {}".format(filename), "cyan")


    def print_room(self, room_name):
        """ Prints the names of all the people in room_name on the screen """
        all_rooms = self.offices + self.l_spaces
        try:
            for one_room in all_rooms:
                if room_name.upper() in [room.room_name for room in all_rooms] and \
                room_name.upper() == one_room.room_name:
                    output = "Occcupants in %s:" % one_room.room_name.upper() + "\n"
                    if len(one_room.current_occupants) == 0:
                        output += "Empty"
                    output += ", ".join(one_room.current_occupants)
            return colored(output, "blue")
        except:
            return colored("Room not found", "red")


    def save_state(self, database=None):
        """ Persists all the data stored in the app to a SQLite database.
        Specifying the --db parameter explicitly stores the data in the
        sqlite_database specified """
        all_rooms = self.offices + self.l_spaces
        everyone = self.fellows + self.staff
        if database is None:
            database = "amity.db"
        else:
            if database[-3:] != ".db":
                database += ".db"
        engine = create_engine('sqlite:///' + database)
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        session.query(RoomModel).delete()
        session.query(PersonModel).delete()

        for room in all_rooms:
            save_room = RoomModel(
                name=room.room_name,
                room_type=room.room_type,
            )

            session.add(save_room)
            session.commit()

        for person in everyone:
            if isinstance(person, Fellow):
                save_person = PersonModel(
                    person_id=person.the_id,
                    name=person.the_name,
                    role="FELLOW",
                    office_space=person.allocated,
                    living_space=person.accommodated
                )
            else:
                save_person = PersonModel(
                    person_id=person.the_id,
                    name=person.the_name,
                    role="STAFF",
                    office_space=person.allocated,
                    living_space=None
                )

            session.add(save_person)
            session.commit()

        return colored("Data saved to %s successfully!" %database, "cyan")


    def load_state(self, db_name):# this doesn't work atm
        """This method loads data from the db
                into the application
                """
        if not os.path.isfile("{}.db".format(db_name)):
            return colored("The database does not exist!", "red")

        if db_name[-3:] != ".db":
            db_name += ".db"

        engine = create_engine('sqlite:///' + db_name)
        Base.metadata.bind = engine
        DBsession = sessionmaker(bind=engine)
        session = DBsession()
        try:
            all_rooms = session.query(RoomModel).all()
            everyone = session.query(PersonModel).all()
        except:
            return colored("This file is in wrong format", "red")

        all_people = self.fellows + self.staff
        cumulative_rooms = self.offices + self.l_spaces
        output = ""

        for room in all_rooms:
            if room.name not in [one_room.room_name for one_room in cumulative_rooms]:
                if room.room_type == "OFFICE":
                    office = Office(room.name)
                    self.offices.append(office)
                    people_in_room = session.query(PersonModel.name).filter(
                        PersonModel.office_space == room.name).all()
                    people_in_room = [str(i[0]) for i in people_in_room]
                    office.current_occupants = people_in_room
                else:
                    l_s = LivingSpace(room.name)
                    self.l_spaces.append(l_s)
                    people_in_room = session.query(PersonModel.name).filter(
                        PersonModel.living_space == room.name).all()
                    people_in_room = [str(i[0]) for i in people_in_room]
                    l_s.current_occupants = people_in_room
            else:
                output += colored("The room: %s couldn't be loaded as it already exists\n"%room.name, "yellow")

        for person in everyone:
            if person.person_id not in [one_person.the_id for one_person in all_people]:
                if person.role == "STAFF":
                    staff = Staff(person.person_id, person.name)
                    self.staff.append(staff)
                    staff.allocated = person.office_space
                else:
                    fellow = Fellow(person.person_id, person.name)
                    self.fellows.append(fellow)
                    fellow.allocated = person.office_space
                    fellow.accommodated = person.living_space
            else:
                output += colored("The person: %s could not be loaded as they already exist\n"%person.name, "yellow")

        return colored("Data loaded successfully!\n", "cyan") + output

    def remove_room(self, room_name):
        """ Removes room (by room name) from Amity"""
        all_rooms = self.offices + self.l_spaces
        all_people = self.fellows + self.staff
        room_name = room_name.upper()

        if room_name not in [room.room_name for room in all_rooms]:
            return colored("Room: %s not in Amity" % room_name, "red")
        else:
            the_room = [room for room in all_rooms if room.room_name == room_name]
            the_room = the_room[0]

            if isinstance(the_room, Office):
                for person in all_people:
                    if person.allocated == room_name:
                        person.allocated = None
                self.offices.remove(the_room)
            else:
                for person in self.fellows:
                    if person.accommodated == room_name:
                        person.accommodated = None
                self.l_spaces.remove(the_room)

            return colored("Room: %s has been deleted from Amity!"%room_name, "magenta")

    def remove_person(self, identifier):
        """ Removes a person from Amity"""
        all_people = self.fellows + self.staff
        all_rooms = self.offices + self.l_spaces

        try:
            identifier = int(identifier)
        except ValueError:
            return colored("Use Id's for identifying a person, NOT name", "yellow")
        # list_ids = [person.the_id for person in all_people]
        deleted_person = [
            person for person in all_people if identifier == int(person.the_id)
        ]
        if len(deleted_person) == 0:
            return colored("This person does not exist", "red")

        person_room = [
            room for room in all_rooms if deleted_person[0].the_name in room.current_occupants
        ]

        if len(person_room) == 1:
            person_room[0].current_occupants.remove(deleted_person[0].the_name)

        if len(person_room) == 2:
            person_room[0].current_occupants.remove(deleted_person[0].the_name)
            person_room[1].current_occupants.remove(deleted_person[0].the_name)

        if isinstance(deleted_person[0], Staff):
            self.staff.remove(deleted_person[0])
        else:
            self.fellows.remove(deleted_person[0])


        return colored("{} has been successfully deleted from Amity."\
        .format(deleted_person[0].the_name), "magenta")
