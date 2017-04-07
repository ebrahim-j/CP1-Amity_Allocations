""" Tests for apps """
import os
import unittest
from amity import Amity
from person import Person, Staff, Fellow
from rooms import Room, Office, LivingSpace


offices = ["asgard", "mtaani"]
livingspaces = ["statehouse"]
rooms = offices + livingspaces
people_id = [1,2,3,4,5,6,7]
fellows = ["wonderwoman", "hulk"]
staff = ["strange"]


class TestCreateRoom(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()

    #test_if_can_add_more than one room
    #test_if_duplicate_entries_not_added

    def test_whether_office_already_exists(self):
        create1 = self.amity.create_room("O", "asgard")
        self.assertEqual("Room already exists", create1, msg="Duplicate room is being created")

    def test_if_office_created(self):
        self.amity.create_room("O", "cave")
        self.assertIn("cave", offices, msg="Office CANNOT be created successfully")

    def test_whether_livingspace_already_exists(self):
        create1 = self.amity.create_room("L", "statehouse")
        self.assertEqual("Room already exists", create1,  msg="Duplicate room is being created")

    def test_if_livingspace_created(self):
        self.amity.create_room("L", "cave")
        self.assertIn("cave", livingspaces, msg="Living Space CANNOT be created successfully")

class TestAddPerson(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()

    def test_whether_fellow_already_exists(self):
        create = self.amity.add_person("WONDERWOMAN", "FELLOW", "Y")
        self.assertEqual("Person already exists", create, msg="Duplicate person being created")

    #test_if_person_identifier_exists
    ## what if 2 people have the same name?

    def test_if_fellow_added(self):
        count = len(self.amity.fellows)
        create = self.amity.add_person("WOLVERINE", "FELLOW", "Y")
        self.assertEqual(len(self.amity.fellows), count + 1, msg="Fellow CANNOT be added successfully")


    def test_whether_staff_already_exists(self):
        create = self.amity.add_person("STRANGE", "STAFF", "N")
        self.assertEqual("Person already exists", create, msg="Duplicate person being created")

    def test_if_staff_added(self):
        count = len(self.amity.staff)
        self.amity.add_person("CYBORG", "STAFF", "N")
        self.assertEqual(len(self.amity.staff), count + 1, msg="Staff CANNOT be added successfully") 

class TestReallocatePerson(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
 #test if staff can't be reallocated to a livingspace


    def test_whether_person_id_valid(self):
        self.assertTrue(self.person.identifier in people_id, msg="Person (ID) does NOT exist")

    def test_if_newroom_exists(self):
        self.assertTrue(self.room.name in rooms, msg="This room (name) does NOT exist")

    def test_newroom_is_not_full(self):
        self.assertTrue(self.room.max_capacity > len(self.room.current_occupants), msg="Room may be full")

    def test_if_reallocation_successful(self):
        self.assertTrue(self.person.name in self.room.current_occupants, msg="Person could NOT be added to room")


class TestLoadPeople(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()

    def test_file_created(self):
        self.assertTrue(os.path.exists("file.txt")) #change filename

    def test_if_file_is_not_already_open(self):
        self.assertEqual(self.amity.load_people(), "file is already opened", msg="File not closed being reopened") #to correct for with parameter

    def test_if_file_does_not_exists(self):
        self.assertEqual(self.amity.load_people(), "file does not exist")

    def test_whether_input_is_txt_file(self):
        pass

    def test_if_input_file_is_not_blank(self):
        self.assertEqual(self.amity.load_people(), "File may be empty or in incorrect format")

    def test_if_input_file_in_correct_format(self):
        self.assertEqual(self.amity.load_people(), "File may be empty or in incorrect format")

    # def test_if_people_added_successfully(self):
    #     pass
    #Test if the number of people in the file are the same number by which the dict/db count has increased


class TestPrintAllocations(unittest.TestCase):

        #     def write_lamb(outfile):
        #     outfile.write("Mary had a little lamb.\n")


        # if __name__ == '__main__':
        #     with open(sys.argv[1], 'w') as outfile:
        #         write_lamb(outfile)



        # ##File test_lamb.py
        # import unittest
        # from io import StringIO

        # import lamb


        # class LambTests(unittest.TestCase):
        #     def test_lamb_output(self):
        #         outfile = StringIO()
        #         # NOTE: Alternatively, for Python 2.6+, you can use
        #         # tempfile.SpooledTemporaryFile, e.g.,
        #         #outfile = tempfile.SpooledTemporaryFile(10 ** 9)
        #         lamb.write_lamb(outfile)
        #         outfile.seek(0)
        #         content = outfile.read()
        #         self.assertEqual(content, "Mary had a little lamb.\n")

    def setUp(self):
        #query through db to collect all allocated people
        pass

    def test_file_created(self):
        self.assertTrue(os.path.exists("file.txt")) #change filename



class TestPrintUnallocated(unittest.TestCase):

    def setUp(self):
        #query through db to collect all unallocated people
        pass

    def test_file_created(self):
        self.assertTrue(os.path.exists("file.txt")) #change filename

class TestPrintRoom(unittest.TestCase):

    def setUp(self):
        self.room = Room("statehouse")
        self.person = Person()
        self.amity = Amity()
        self.amity.reallocate_person(1, "statehouse")

    def test_if_room_exists(self):
        self.assertTrue(self.room.name in rooms, msg="Room does NOT exist")

    def test_room_prints_all_members(self):
        self.assertTrue(len(self.room.current_occupants) == 1, msg="All members not printed successfully")



class TestSaveState(unittest.TestCase):
    def setUp(self):
        amity = Amity()
        amity.save_state() #refactor to accept an optional argument for filename

    def test_file_created(self):
        self.assertTrue(os.path.exists("file.db")) #change filename


class TestLoadState(unittest.TestCase):
    def setUp(self):
        amity = Amity()
        amity.load_people() #refactor to accept an optional argument for filename

    def test_file_created(self):
        self.assertTrue(os.path.exists("file.db")) #change filename



if __name__ == '__main__':
    unittest.main()
