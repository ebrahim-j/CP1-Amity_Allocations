""" Tests for apps """
import os
import unittest
from amity import Amity
from models.person import Person, Staff, Fellow
from models.rooms import Room, Office, LivingSpace


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
    #test_if_can_add_more than one room
    #test_if_duplicate_entries_not_added

    def test_whether_office_already_exists(self):
        create1 =self.amity.create_room("O", "asgard")
        create2 =self.amity.create_room("O", "asgard")
        self.assertEqual("Room name: ASGARD already exists", create2, msg="Duplicate room is being created")

    def test_if_office_created(self):
        self.assertEqual(self.amity.create_room("O", "cave"), "We have successfully created a new office called: CAVE", msg="Office CANNOT be created successfully")

    def test_whether_livingspace_already_exists(self):
        create1 =self.amity.create_room("L", "statehouse")
        create2 =self.amity.create_room("L", "statehouse")
        self.assertEqual("Room name: STATEHOUSE already exists", create2,  msg="Duplicate room is being created")

    def test_if_livingspace_created(self):
        self.assertEqual(self.amity.create_room("L", "cave"), "New living quarters ( CAVE ) successfully created!", msg="Office CANNOT be created successfully")

    # def test_whether_fellow_already_exists(self):
    #     create =self.amity.add_person("WONDER","WOMAN", "FELLOW", "Y")
    #     create1 =self.amity.add_person("WONDER", "WOMAN", "FELLOW", "N")
    #     self.assertEqual("Person already exists", create1)#, msg="Duplicate person being created"

    #test_if_person_identifier_exists, 2 people with the same name?

    def test_if_fellow_added(self):
        room =self.amity.create_room("o", "oculus")
        ls =self.amity.create_room("l", "london")
        create =self.amity.add_person("WOLVERINE", "LOGAN", "FELLOW", "Y")
        person_identity = [person.the_id for person in self.amity.fellows]
        person_identity = person_identity[0]
        self.assertEqual(create, "(%s): WOLVERINE LOGAN has been appointed to OCULUS and will live in LONDON"%person_identity, msg="Fellow CANNOT be added successfully")

    # def test_whether_staff_already_exists(self):
    #     create =self.amity.add_person("DOCTOR", "STRANGE", "STAFF", "N")
    #     create1 =self.amity.add_person("DOCTOR", "STRANGE", "STAFF", "N")
    #     self.assertEqual("Person already exists", create1)#, msg="Duplicate person being created"

    def test_if_staff_added(self):
        create =self.amity.add_person("THE","CYBORG", "STAFF")
        person_identity = [person.the_id for person in self.amity.staff]
        person_identity = person_identity[0]
        self.assertEqual(create, "Welcome (%s) THE CYBORG, You will be allocated an office as soon as we have space"%person_identity, msg="Staff CANNOT be added successfully" )

    def test_if_randomly_allocated(self):
       self.amity.create_room("o", "Mombasa")
       self.amity.add_person("THE","CYBORG", "STAFF", "N")
       self.assertTrue("THE CYBORG" in self.amity.offices[0].current_occupants)


    def test_if_newroom_doesnt_exists(self):
       self.amity.add_person("THE","CYBORG", "STAFF", "N")
       person_identity = [person.the_id for person in self.amity.staff]
       person_identity = person_identity[0]
       reallocate =self.amity.reallocate_person(person_identity, "Mombasa")
       self.assertEqual(reallocate, "This room does not exist. (Make sure you spell check your room names)", msg="This room (name) does NOT exist")

    def test_if_identifier_doesnt_exist(self):
       self.amity.create_room("o", "Mombasa")
       reallocate =self.amity.reallocate_person(99999, "Mombasa")
       self.assertEqual(reallocate, "This person cannot be identified", msg="Non existant person is being reallocated")

    def test_newroom_is_not_full(self):
       self.amity.create_room("l", "Mombasa")
       self.amity.add_person("THE","ROCK","FELLOW", "Y")
       self.amity.add_person("THE","MACE","FELLOW", "Y")
       self.amity.add_person("THE","CYBORG","FELLOW", "Y")
       self.amity.add_person("THE","UNDERTAKER","FELLOW", "Y")
       self.amity.add_person("THE","THING","FELLOW", "Y")
       person_identity = [person.the_id for person in self.amity.fellows if person.the_name == "THE THING"]
       person_identity = person_identity[0]
       reallocate =self.amity.reallocate_person(person_identity, "Mombasa")
       self.assertEqual(reallocate, "Sorry, room is full", msg="Person is curently being allocated to a full room")


    def test_if_reallocation_successful(self):
       self.amity.create_room("l", "Mombasa")
       self.amity.add_person("THE","ROCK","FELLOW", "Y")
       self.amity.create_room("l", "Mogadishu")
       person_identity = [person.the_id for person in self.amity.fellows]
       person_identity = person_identity[0]
       reallocate =self.amity.reallocate_person(person_identity, "Mogadishu")
       self.assertEqual(reallocate, "THE ROCK has been reallocated to MOGADISHU", msg="Person could NOT be added to room")

    def test_people_loaded(self):
       response = self.amity.load_people()
       print(response)
       self.assertEqual(response, "File loaded successfully", msg="File NOT created successfully")

    # def test_if_file_does_not_exists(self):
    #     response = self.amity.load_people("kbdk.txt")
    #     self.assertEqual(response, "File does not exist", msg="Non-existing file is being tried to load")

    # def test_whether_input_is_txt_file(self):
    #     response =self.amity.load_people("text.db")
    #     self.assertEqual(response, "System can only load people from a text file", msg="System is loading other files besides text files")

    # def test_if_input_file_is_not_blank(self):
    #     response =self.amity.load_people("empty.txt")
    #     print(response)
    #     self.assertEqual(response, "File may be empty or in incorrect format", msg="System doesn't handle for empty files")

    # def test_if_input_file_in_correct_format(self):
    #     self.assertEqual(self.amity.load_people("incorrect.txt"), 'Inaccurate information. Double check your file')#check this


    def test_allocated_file_created(self):
        response = self.amity.print_allocations("allocated.txt")
        self.assertEqual(response, "Data has been successfully saved to allocated.txt")
        self.assertTrue(os.path.exists("allocated.txt"))

    def test_if_room_exists(self):
        response =self.amity.print_room("Manchester")
        self.assertEqual(response, "Room not found", msg="System printing room which is non-existant")

    def test_room_prints_all_members(self):
       self.amity.create_room("l", "Mombasa")
       self.amity.add_person("THE","THING","FELLOW", "Y")
       self.amity.add_person("THE","MACE","FELLOW", "Y")
       self.amity.add_person("THE","ROCK","FELLOW", "Y")
       response =self.amity.print_room("Mombasa")
       self.assertTrue(("THE THING" and "THE MACE" and "THE ROCK") in response, msg="All members not printed successfully")


    def test_dbfile_created(self):
        self.amity.save_state("file.db")
        self.assertTrue(os.path.exists("file.db")) #change filename



if __name__ == '__main__':
    unittest.main()
