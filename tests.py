""" Tests for apps """
import os
import unittest
from amity import Amity
from person import Person, Staff, Fellow
from rooms import Room, Office, LivingSpace


amity = Amity()
class TestAmity(unittest.TestCase):


    #test_if_can_add_more than one room
    #test_if_duplicate_entries_not_added

    def test_whether_office_already_exists(self):
        create1 = amity.create_room("O", "asgard")
        create2 = amity.create_room("O", "asgard")
        self.assertEqual("Office already exists", create2, msg="Duplicate room is being created")

    def test_if_office_created(self):
        self.assertEqual(amity.create_room("O", "cave"), "We have successfully created a new office called: CAVE", msg="Office CANNOT be created successfully")

    def test_whether_livingspace_already_exists(self):
        create1 = amity.create_room("L", "statehouse")
        create2 = amity.create_room("L", "statehouse")
        self.assertEqual("Living Space already exists", create2,  msg="Duplicate room is being created")

    def test_if_livingspace_created(self):
        self.assertEqual(amity.create_room("L", "cave"), "New living quarters ( CAVE ) successfully created!", msg="Office CANNOT be created successfully")

    def test_whether_fellow_already_exists(self):
        create = amity.add_person("WONDER","WOMAN", "FELLOW", "Y")
        create1 = amity.add_person("WONDER", "WOMAN", "FELLOW", "N")
        self.assertEqual("Person already exists", create1, msg="Duplicate person being created")

    #test_if_person_identifier_exists, 2 people with the same name?

    def test_if_fellow_added(self):
        room = amity.create_room("o", "oculus")
        ls = amity.create_room("l", "london")
        create = amity.add_person("WOLVERINE", "LOGAN", "FELLOW", "Y")
        self.assertEqual(create, "WOLVERINE LOGAN has been appointed to OCULUS and will live in LONDON", msg="Fellow CANNOT be added successfully")

    def test_whether_staff_already_exists(self):
        create = amity.add_person("DOCTOR", "STRANGE", "STAFF", "N")
        self.assertEqual("Person already exists", create, msg="Duplicate person being created")

    def test_if_staff_added(self):
        create = amity.add_person("THE","CYBORG", "STAFF")
        self.assertEqual(create, "Welcome THE CYBORG, You will be allocated an office as soon as we have space", msg="Staff CANNOT be added successfully") 

    def test_if_randomly_allocated(self):
        amity.create_room("o", "Mombasa")
        amity.add_person("THE","CYBORG", "STAFF", "N")
        self.assertTrue("THE CYBORG" in amity.offices[0].current_occupants)

    def test_whether_nonexisting_person_not_added(self):
        amity.create_room("o", "Mombasa")
        amity.add_person("THE","CYBORG", "STAFF", "N")
        amity.create_room("o", "Mogadishu")
        reallocate = amity.reallocate_person("THE MACE", "Mogadishu")
        self.assertEqual(reallocate, "This person cannot be identified", msg="invalid person_name being used")

    def test_if_newroom_doesnt_exists(self):
        amity.add_person("THE","CYBORG", "STAFF", "N")
        reallocate = amity.reallocate_person("THE CYBORG", "Mombasa")
        self.assertEqual(reallocate, "This room does not exist. (Make sure you spell check your room names)", msg="This room (name) does NOT exist")

    def test_if_identifier_doesnt_exist(self):
        amity.create_room("o", "Mombasa")
        reallocate = amity.reallocate_person("THE ROCK", "Mombasa")
        self.assertEqual(reallocate, "This person cannot be identified", msg="Non existant person is being reallocated")

    def test_newroom_is_not_full(self):
        amity.create_room("l", "Mombasa")
        amity.add_person("THE","ROCK","FELLOW", "Y")
        amity.add_person("THE","MACE","FELLOW", "Y")
        amity.add_person("THE","CYBORG","FELLOW", "Y")
        amity.add_person("THE","UNDERTAKER","FELLOW", "Y")
        amity.add_person("THE","THING","FELLOW", "Y")

        reallocate = amity.reallocate_person("THE THING", "Mombasa")
        self.assertEqual(reallocate, "Sorry, room is full", msg="Person is curently being allocated to a full room")


    def test_if_reallocation_successful(self):
        amity.create_room("l", "Mombasa")
        amity.add_person("THE","ROCK","FELLOW", "Y")
        amity.create_room("l", "Mogadishu")
        reallocate = amity.reallocate_person("THE ROCK", "Mogadishu")
        self.assertEqual(reallocate, "THE ROCK has been reallocated to Mogadishu")#, msg="Person could NOT be added to room"

    def test_file_created(self):
        amity.load_people("text.txt")
        self.assertTrue(os.path.exists("text.txt"), msg="File NOT created successfully")

    def test_if_file_does_not_exists(self):
        response = amity.load_people("kbdk.txt")
        self.assertEqual(response, "File does not exist", msg="Non-existing file is being tried to load")

    def test_whether_input_is_txt_file(self):
        response = amity.load_people("text.db")
        self.assertEqual(response, "System can only load people from a text file", msg="System is loading other files besides text files")

    def test_if_input_file_is_not_blank(self):
        response = amity.load_people("empty.txt")
        self.assertEqual(response, "File may be empty or in incorrect format", msg="System doesn't handle for empty files")

    def test_if_input_file_in_correct_format(self):
        self.assertEqual(amity.load_people(), "File may be empty or in incorrect format")#check this

    def test_if_people_added_successfully(self):
        response = amity.load_people("text.txt")
        self.assertEqual(response, "File loaded successfully", msg="File not loading successfully")

    def test_allocated_file_created(self):
        self.assertTrue(os.path.exists("allocated.txt")) #change filename

    def test_if_room_exists(self):
        response = amity.print_room("Manchester")
        self.assertEqual(response, "Room not found", msg="System printing room which is non-existant")

    def test_room_prints_all_members(self):
        amity.create_room("l", "Mombasa")
        amity.add_person("THE","THING","FELLOW", "Y")
        amity.add_person("THE","MACE","FELLOW", "Y")
        amity.add_person("THE","ROCK","FELLOW", "Y")
        response = amity.print_room("Mombasa")
        self.assertTrue(("THE THING" and "THE MACE" and "THE ROCK") in response, msg="All members not printed successfully")


    def test_dbfile_created(self):
        self.assertTrue(os.path.exists("file.db")) #change filename



if __name__ == '__main__':
    unittest.main()
