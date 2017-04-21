""" Functions consisted in class Amity """
import os
from models.person import Fellow, Staff
from models.rooms import Office, LivingSpace, Room
from random import randint, choice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.dbModels import RoomModel, PersonModel, Base

# correct for .lower() or likewise entries


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

    def add_person(self, firstname, lastname, role, wants_accommodation='N'):
        # if not name.isalpha() or not role.isalpha() or not wants_accommodation.isalpha():
        # return "Please ensure you don't have digits in name, role or
        # accommodation"
        all_people = self.fellows + self.staff
        identifier = randint(1, 9999)  # query the db?
        name = firstname + " " + lastname
        if name.upper() in [person.the_name.upper() for person in all_people]:
            return "Person already exists"
        if role.lower() == "staff":
            wants_accommodation = "N"
            person = Staff(identifier, name)
            self.staff.append(person)
            office_selected = Amity.randomly_allocate_office(self)
            if office_selected == False:
                return "Welcome %s, You will be allocated an office as soon as we have space" % person.the_name
            office_selected.current_occupants.append(person.the_name)
            person.allocated = office_selected.room_name
            return "%s has been allocated to %s" % (person.the_name, office_selected.room_name)
        elif role.lower() == "fellow":
            if wants_accommodation.upper() == "N" or wants_accommodation.upper() == "NO":
                person = Fellow(identifier, name)
                self.fellows.append(person)
                office_selected = Amity.randomly_allocate_office(self)
                if office_selected == False:
                    return "Welcome (%s) %s, You will be allocated an office as soon as we have space" % (person.the_name, person.the_name)
                office_selected.current_occupants.append(person.the_name)
                person.allocated = office_selected.room_name
                return "(%s): %s has been allocated to %s" % (
                    person.the_name, person.the_name, office_selected.room_name)
            elif wants_accommodation.upper() == "Y" or wants_accommodation.upper() == "YES":
                person = Fellow(identifier, name)
                self.fellows.append(person)
                office_selected = Amity.randomly_allocate_office(self)
                ls_selected = Amity.randomly_allocate_ls(self)
                if office_selected == False and ls_selected == False:
                    return "Welcome (%s) %s, You will be allocated an office and a Living Space as soon as we have space" % (
                        person.the_name, person.the_name)
                elif office_selected == False and ls_selected != False:
                    ls_selected.current_occupants.append(person.the_name)
                    person.accommodated = ls_selected.room_name
                    return "Welcome (%s) %s, You will live in %s and will be allocated an office as soon as we have space" % (
                        person.the_name, person.the_name, ls_selected.room_name)
                elif ls_selected == False and office_selected != False:
                    office_selected.current_occupants.append(person.the_name)
                    person.allocated = office_selected.room_name
                    return "Welcome (%s) %s, You have been allocated to %s. You will be assigned a living space as soon as we have room" % (
                        person.the_name, person.the_name, office_selected.room_name)
                else:
                    office_selected.current_occupants.append(person.the_name)
                    person.allocated = office_selected.room_name
                    ls_selected.current_occupants.append(person.the_name)
                    person.accommodated = ls_selected.room_name
                    return "%s has been appointed to %s and will live in %s" % (person.the_name.upper(), office_selected.room_name.upper(), ls_selected.room_name.upper())
            else:
                return "I don't know whether you want accomodation or not. (Reply with Y or Yes, N or No) "
        else:
            return "Person can either be Staff or Fellow"


    def create_room(self, prefix, name):
        """instantiates a living space or office based on prefix"""
        # check for edge cases here
        if not prefix.isalpha():
            return "Room type cannot be in digits"
        if prefix.lower() == "office" or prefix.lower() == "o":  # try regex
            if name.upper() in [room.room_name.upper() for room in self.offices]:
                return "Office already exists"
            room = Office(name)
            self.offices.append(room)
            result = "We have successfully created a new office called: %s" % room.room_name.upper()
            return result
        elif prefix.lower() == "living space" or prefix.lower() == "livingspace" or prefix.lower() == "l" or prefix.lower() == "ls":  # try regex
            if name.upper() in [room.room_name.upper() for room in self.l_spaces]:
                return "Living Space already exists"
            room = LivingSpace(name)
            self.l_spaces.append(room)
            result = "New living quarters ( %s ) successfully created!" % room.room_name.upper(
            )
            return result
        else:
            return "This"


    def reallocate_person(self, person_name, new_room_name):
        """ Reallocates a person with person_identifier to new_room_name """
        employees = self.fellows + self.staff
        all_rooms = self.offices + self.l_spaces
        # see for someone who doesn't have a room kabisa
        for individual in employees:
            if individual.the_name == person_name:
                # check for when person is alloccated to same room
                if new_room_name.lower() not in [room.room_name.lower() for room in all_rooms]:
                    return "This room does not exist. (Make sure you spell check your room names)"
                elif new_room_name.lower() in [room.room_name.lower() for room in self.offices]:
                    for room in self.offices:
                        if room.room_name == new_room_name and not room.room_has_space():
                            return "Sorry, room is full"
                    for room in self.offices:
                        if individual.the_name in room.current_occupants:
                            room.current_occupants.remove(
                                individual.the_name)
                    for room in self.offices:
                        if room.room_name == new_room_name and room.room_has_space():
                            room.current_occupants.append(
                                individual.the_name)
                            individual.allocated = new_room_name
                    return "%s has been reallocated to %s" % (individual.the_name, new_room_name)
                elif not isinstance(individual, Staff) and new_room_name.lower() in [room.room_name.lower() for room in self.l_spaces]:
                    for room in self.l_spaces:
                        if room.room_name == new_room_name and not room.room_has_space():
                            return "Sorry, room is full"
                    for room in self.l_spaces:
                            if individual.the_name in room.current_occupants:
                                room.current_occupants.remove(
                                    individual.the_name)
                    for room in self.l_spaces:
                            if room.room_name == new_room_name and room.room_has_space():
                                room.current_occupants.append(
                                    individual.the_name)
                                individual.accommodated = new_room_name
                    return "%s has been reallocated to %s" % (individual.the_name, new_room_name)
                elif isinstance(individual, Staff) and new_room_name.lower() in [room.room_name.lower() for room in self.l_spaces]:
                    return "Cannot allocate staff to a living Space"

        return "This person cannot be identified"


    def load_people(self, filepath):
        """ Adds people to rooms from a txt file """

        if filepath[-4:] != '.txt':
            return "System can only load people from a text file"
        try:
            with open(filepath, 'r') as my_file:
                info = my_file.readlines()
                if len(info) == 0:
                    return "File may be empty or in incorrect format"
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
                        return "Inaccurate information. Double check your file"
                return "File loaded successfully"
        except:
            return "File does not exist"


    def print_allocations(self, filename=None):
        """ Prints a list of allocations.
        Specifying the optional -o option outputs the registered allocations to a txt file """
        output = ""
        if len(self.offices) == 0:
            output = "NO offices added yet!\n"
        else:
            output = "OFFICES:\n" + ("=" * 8 + "\n")
            for room in self.offices:
                output += room.room_name.upper() + "\n" + ("-" * 20 + "\n")
                output += ", ".join(room.current_occupants) + "\n\n"
        if len(self.l_spaces) == 0:
            output += "NO living spaces added yet!"
        else:
            output += "LIVING SPACES:\n" + ("=" * 14 + "\n")
            for room in self.l_spaces:
                output += room.room_name.upper() + "\n" + ("-" * 20 + "\n")
                output += ", ".join(room.current_occupants) + "\n\n"

        if filename is None:
            return output
        else:
            if filename[-4:] != ".txt":
                filename += ".txt"
            with open(filename, 'w+') as my_file:
                my_file.write(output)
            return "Data has been successfully saved to {}".format(filename)


    def print_unallocated(self, filename=None):
        """ Prints a list of unallocated people to the screen.
        Specifying the -o option here outputs the information to the txt file provided """
        unallocated = []
        everyone = self.fellows + self.staff
        for one_person in everyone:
            if one_person.allocated is None:
                unallocated.append([one_person.the_id, one_person.the_name])
            elif not isinstance(one_person, Staff) and one_person.accommodated is None:
                unallocated.append([one_person.the_id, one_person.the_name])

        if len(unallocated) == 0:
            return "Good News! Everyone is allocated"

        output = "The following people are unallocated: \n"
        for person in unallocated:
            output += "%s:- %s\n" % (person[0], person[1])

        if filename is None:
            return output
        else:
            if filename[-4:] != ".txt":
                filename += ".txt"
            with open(filename, 'w+') as my_file:
                my_file.write(output)
            return "Data has been successfully saved to {}".format(filename)


    def print_room(self, room_name):
        """ Prints the names of all the people in room_name on the screen """
        all_rooms = self.offices + self.l_spaces
        try:
            for one_room in all_rooms:
                if room_name in [room.room_name for room in all_rooms] and room_name.lower() == one_room.room_name.lower():
                    output = "Occcupants in %s:" % one_room.room_name.upper() + "\n"
                    output += ", ".join(one_room.current_occupants)
            return output
        except:
            return "Room not found"


    def save_state(self, database=None):
        """ Persists all the data stored in the app to a SQLite database.
        Specifying the --db parameter explicitly stores the data in the
        sqlite_database specified """
        all_rooms = self.offices + self.l_spaces
        everyone = self.fellows + self.staff
        if database == None:
            database = "amity.db"
        else:
            if database[-3:] != ".db":
                database += ".db"
        engine = create_engine('sqlite:///' + database)
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        for room in all_rooms:
            save_room = RoomModel(
                name=room.room_name,
                room_type=room.room_type,
            )
            existing = session.query(RoomModel).filter(
                RoomModel.name == room.room_name).count()
            if not existing:
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
            existing = session.query(PersonModel).filter(
                PersonModel.person_id == person.the_id).count()

            if not existing:
                session.add(save_person)
            session.commit()


    def load_state(self, db_name):
        """This method loads data from the db
                into the application
                """
        if not os.path.isfile("{}.db".format(db_name)):
            return ("The database does not exist!")

        if db_name[-3:] != ".db":
            db_name += ".db"

        engine = create_engine('sqlite:///' + db_name)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        all_rooms = session.query(RoomModel).all()
        everyone = session.query(PersonModel).all()

        for room in all_rooms:
            if room.room_type == "OFFICE":
                office = Office(room.name)
                self.offices.append(office)
                people_in_room = session.query(PersonModel.name).filter(
                    PersonModel.office_space == room.name).all()
                people_in_room = [str(i[0]) for i in people_in_room]
                office.current_occupants = people_in_room
            else:
                ls = LivingSpace(room.name)
                self.l_spaces.append(ls)
                people_in_room = session.query(PersonModel.name).filter(
                    PersonModel.living_space == room.name).all()
                people_in_room = [str(i[0]) for i in people_in_room]
                ls.current_occupants = people_in_room

        for person in everyone:
            if person.role == "STAFF":
                staff = Staff(person.person_id, person.name)
                self.staff.append(staff)
                staff.allocated = str(person.office_space)
            else:
                fellow = Fellow(person.person_id, person.name)
                self.fellows.append(fellow)
                fellow.allocated = str(person.office_space)
                fellow.accommodated = str(person.living_space)
