""" Tests for apps """
import os
import unittest
from amity import Amity
from models.person import Person, Fellow
from models.rooms import Room, Office, LivingSpace


class TestAmity(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()


    def test_if_fellow_added(self):
        room = self.amity.create_room("o", "oculus")
        ls = self.amity.create_room("l", "london")
        create = self.amity.add_person("WOLVERINE", "LOGAN", "FELLOW", "Y")
        person_identity = [person.the_id for person in self.amity.fellows]
        person_identity = person_identity[0]
        self.assertEqual(create, "\x1b[36m(%s): WOLVERINE LOGAN has been appointed to OCULUS and will live in LONDON\x1b[0m" %
                         person_identity, msg="Fellow CANNOT be added successfully")

    def test_staff_added_and_allocated(self):
        self.amity.create_room("o", "dakar")
        response = self.amity.add_person("THE", "MACE", "STAFF")
        person_identity = [person.the_id for person in self.amity.staff]
        person_identity = person_identity[0]
        self.assertEqual(
            response, "\x1b[36m(%s): THE MACE has been allocated to the office DAKAR\x1b[0m" % person_identity)

    def test_if_staff_wants_acc_handled(self):
        response = self.amity.add_person("the", "moneymaker", "staff", "y")
        person_identity = [person.the_id for person in self.amity.staff]
        person_identity = person_identity[0]
        expected = "\x1b[32m(%s) THE MONEYMAKER has been added and will be allocated an office as soon as we have space\x1b[0m\x1b[33m. Staff cannot be allocated a living space\x1b[0m"%person_identity
        self.assertEqual(response, expected)

    def test_if_staff_added_with_no_office(self):
        create = self.amity.add_person("THE", "CYBORG", "STAFF")
        person_identity = [person.the_id for person in self.amity.staff]
        person_identity = person_identity[0]
        self.assertEqual(create, "\x1b[32m(%s) THE CYBORG has been added and will be allocated an office as soon as we have space\x1b[0m" %
                         person_identity, msg="Staff CANNOT be added successfully")

    def test_fellow_doesnt_get_office(self):
        response = self.amity.add_person("THE", "LEGEND", "fellow")
        person_identity = [person.the_id for person in self.amity.fellows]
        person_identity = person_identity[0]
        self.assertEqual(
            response, "\x1b[32m(%s) THE LEGEND has been added and will be allocated an office as soon as we have space\x1b[0m" % person_identity)

    def test_fellow_gets_office(self):
        self.amity.create_room("o", "kili")
        response = self.amity.add_person("THE", "LEGEND", "FELLOW", "N")
        person_identity = [person.the_id for person in self.amity.fellows]
        person_identity = person_identity[0]
        self.assertEqual(
            response, "\x1b[36m(%s): THE LEGEND has been allocated to KILI\x1b[0m" % person_identity)

    def test_fellow_doesnt_get_any_rooms(self):
        response = self.amity.add_person("THE", "LEGEND", "FELLOW", "Y")
        person_identity = [person.the_id for person in self.amity.fellows]
        person_identity = person_identity[0]
        self.assertEqual(
            response, "\x1b[32m(%s) THE LEGEND has been added and will be allocated an office and a Living Space as soon as we have space\x1b[0m" % person_identity)

    def test_fellow_gets_only_office(self):
        self.amity.create_room("o", "kili")
        response = self.amity.add_person("THE", "LEGEND", "FELLOW", "Y")
        person_identity = [person.the_id for person in self.amity.fellows]
        person_identity = person_identity[0]
        self.assertEqual(
            response, "\x1b[33m(%s) THE LEGEND has been allocated to KILI. You will be assigned a living space as soon as we have room\x1b[0m" % person_identity)

    def test_fellow_gets_only_ls(self):
        self.amity.create_room("l", "kili")
        response = self.amity.add_person("THE", "LEGEND", "FELLOW", "Y")
        person_identity = [person.the_id for person in self.amity.fellows]
        person_identity = person_identity[0]
        self.assertEqual(
            response, "\x1b[33m(%s) THE LEGEND will live in KILI and will be allocated an office as soon as we have space\x1b[0m" % person_identity)

    def test_bad_input(self):
        response = self.amity.add_person("ief", "sd", "stuff")
        self.assertEqual(
            response, "\x1b[31mPerson can either be Staff or Fellow\x1b[0m")

    def test_invalid_input(self):
        response = self.amity.add_person("ief", "sd", "fellow", "x")
        self.assertEqual(
            response, "\x1b[31mI don't know whether you want accomodation or not. (Reply with Y or Yes, N or No) \x1b[0m")

    def test_get_empty_people(self):
        response = self.amity.get_everyone()
        self.assertEqual(response, "\x1b[31mNobody in Amity! :'(\x1b[0m")

    def test_get_some_people(self):
        self.amity.add_person("THE", "LEGEND", "FELLOW", "Y")
        self.amity.add_person("THE", "ROCK", "STAFF")
        fellow_id = [person.the_id for person in self.amity.fellows]
        staff_identity = [person.the_id for person in self.amity.staff]
        expected = "\x1b[34m{} | THE LEGEND | Fellow\n\n{} | THE ROCK | Staff\n\n\x1b[0m".format(
            fellow_id[0], staff_identity[0])
        response = self.amity.get_everyone()
        self.assertEqual(response, expected)

    def test_no_digits_in_name(self):
        response = self.amity.create_room("o", "fequjy9")
        self.assertEqual(response, "\x1b[31mRoom cannot have digits\x1b[0m")

    def test_no_digits_in_type(self):
        response = self.amity.create_room("off1ce", "fequjy")
        self.assertEqual(
            response, "\x1b[31mRoom type cannot be in digits\x1b[0m")

    def test_whether_office_already_exists(self):
        create1 = self.amity.create_room("O", "asgard")
        create2 = self.amity.create_room("O", "asgard")
        self.assertEqual("\x1b[31mRoom name: ASGARD already exists\x1b[0m",
                         create2, msg="Duplicate room is being created")

    def test_if_office_created(self):
        self.assertEqual(self.amity.create_room(
            "O", "cave"), "\x1b[36mWe have successfully created a new office called: CAVE\x1b[0m", msg="Office CANNOT be created successfully")

    def test_whether_livingspace_already_exists(self):
        create1 = self.amity.create_room("L", "statehouse")
        create2 = self.amity.create_room("L", "statehouse")
        self.assertEqual("\x1b[31mRoom name: STATEHOUSE already exists\x1b[0m",
                         create2,  msg="Duplicate room is being created")

    def test_if_livingspace_created(self):
        self.assertEqual(self.amity.create_room(
            "L", "cave"), "\x1b[36mNew living quarters ( CAVE ) successfully created!\x1b[0m", msg="Office CANNOT be created successfully")

    def test_cant_be_reallocated_to_same_office(self):
        self.amity.create_room("o", "durban")
        self.amity.add_person("THE", "CYBORG", "STAFF", "N")
        person_identity = [person.the_id for person in self.amity.staff]
        person_identity = person_identity[0]
        response = self.amity.reallocate_person(person_identity, "durban")
        self.assertEqual(
            response, "\x1b[33mTHE CYBORG already in DURBAN\x1b[0m")

    def test_cant_be_reallocated_to_same_ls(self):
        self.amity.create_room("ls", "durban")
        self.amity.add_person("THE", "CYBORG", "Fellow", "Y")
        person_identity = [person.the_id for person in self.amity.fellows]
        person_identity = person_identity[0]
        response = self.amity.reallocate_person(person_identity, "durban")
        self.assertEqual(
            response, "\x1b[33mTHE CYBORG already in DURBAN\x1b[0m")

    def test_full_office(self):
        self.amity.add_person("the", "undertaker", "fellow", "n")
        person_identity = [person.the_id for person in self.amity.fellows]
        person_identity = person_identity[0]
        self.amity.create_room("office", "Malindi")
        self.amity.load_people()
        response = self.amity.reallocate_person(person_identity, "Malindi")
        self.assertEqual(response, "\x1b[32mSorry, room is full\x1b[0m")

    def test_if_newroom_doesnt_exists(self):
        self.amity.add_person("THE", "CYBORG", "STAFF", "N")
        person_identity = [person.the_id for person in self.amity.staff]
        person_identity = person_identity[0]
        reallocate = self.amity.reallocate_person(person_identity, "Mombasa")
        self.assertEqual(reallocate, "\x1b[31mThis room does not exist. (Make sure you spell check your room names)\x1b[0m",
                         msg="This room (name) does NOT exist")

    def test_if_identifier_doesnt_exist(self):
        self.amity.create_room("o", "Mombasa")
        reallocate = self.amity.reallocate_person(99999, "Mombasa")
        self.assertEqual(reallocate, "\x1b[31mThis person cannot be identified\x1b[0m",
                         msg="Non existant person is being reallocated")

    def test_ls_is_not_full(self):
        self.amity.create_room("l", "Mombasa")
        self.amity.add_person("THE", "ROCK", "FELLOW", "Y")
        self.amity.add_person("THE", "MACE", "FELLOW", "Y")
        self.amity.add_person("THE", "CYBORG", "FELLOW", "Y")
        self.amity.add_person("THE", "UNDERTAKER", "FELLOW", "Y")
        self.amity.add_person("THE", "THING", "FELLOW", "Y")
        person_identity = [
            person.the_id for person in self.amity.fellows if person.the_name == "THE THING"]
        person_identity = person_identity[0]
        reallocate = self.amity.reallocate_person(person_identity, "Mombasa")
        self.assertEqual(reallocate, "\x1b[32mSorry, room is full\x1b[0m",
                         msg="Person is curently being allocated to a full room")

    def test_if_ls_reallocation_successful(self):
        self.amity.create_room("l", "Mombasa")
        self.amity.add_person("THE", "ROCK", "FELLOW", "Y")
        self.amity.create_room("l", "Mogadishu")
        person_identity = [person.the_id for person in self.amity.fellows]
        person_identity = person_identity[0]
        reallocate = self.amity.reallocate_person(person_identity, "Mogadishu")
        self.assertEqual(reallocate, "\x1b[36mTHE ROCK has been reallocated to MOGADISHU\x1b[0m",
                         msg="Person could NOT be added to room")

    def test_if_office_reallocation_successful(self):
        self.amity.create_room("o", "Mombasa")
        self.amity.add_person("THE", "ROCK", "FELLOW", "Y")
        self.amity.create_room("o", "Mogadishu")
        person_identity = [person.the_id for person in self.amity.fellows]
        person_identity = person_identity[0]
        reallocate = self.amity.reallocate_person(person_identity, "Mogadishu")
        self.assertEqual(reallocate, "\x1b[36mTHE ROCK has been reallocated to MOGADISHU\x1b[0m",
                         msg="Person could NOT be added to room")

    def test_staff_allocation_to_ls(self):
        self.amity.add_person("THE", "ROCK", "Staff")
        self.amity.create_room("l", "Haba")
        person_identity = [person.the_id for person in self.amity.staff]
        person_identity = person_identity[0]
        response = self.amity.reallocate_person(person_identity, "haba")
        self.assertEqual(
            response, "\x1b[31mCannot allocate staff to a living Space\x1b[0m")

    def test_people_loaded(self):
        response = self.amity.load_people()
        self.assertEqual(response, "\x1b[36mFile loaded successfully\x1b[0m",
                         msg="File NOT created successfully")

    def test_empty_file_load(self):
        response = self.amity.load_people("empty")
        self.assertEqual(response, "\x1b[33mFile is empty\x1b[0m")

    def test_incorrect_format(self):
        response = self.amity.load_people("incorrect")
        self.assertEqual(response, "\x1b[31mInaccurate information. Double check your file\x1b[0m")

    def test_nonexisting_file(self):
        response = self.amity.load_people("ebhkj")
        self.assertEqual(response, "\x1b[31mFile does not exist\x1b[0m")

    def test_if_room_exists(self):
        response = self.amity.print_room("Manchester")
        self.assertEqual(response, "\x1b[31mRoom not found\x1b[0m",
                         msg="System printing room which is non-existant")

    def test_room_prints_all_members(self):
        self.amity.create_room("l", "Mombasa")
        self.amity.add_person("THE", "THING", "FELLOW", "Y")
        self.amity.add_person("THE", "MACE", "FELLOW", "Y")
        self.amity.add_person("THE", "ROCK", "FELLOW", "Y")
        response = self.amity.print_room("Mombasa")
        self.assertTrue(("THE THING" and "THE MACE" and "THE ROCK")
                        in response, msg="All members not printed successfully")

    def test_print_empty_list(self):
        self.amity.create_room("o", "Juja")
        response = self.amity.print_room("juja")
        self.assertEqual(response, "\x1b[34mOcccupants in JUJA:\nEmpty\x1b[0m")

    def test_prints_allocations_on_screen(self):
        response = self.amity.print_allocations()
        self.assertEqual(
            response, "\x1b[34mNO offices added yet!\nNO living spaces added yet!\x1b[0m")

    def test_prints_allocations_to_file(self):
        response = self.amity.print_allocations("testfile")
        self.assertEqual(
            response, "\x1b[36mData has been successfully saved to testfile.txt\x1b[0m")

    def test_prints_empty(self):
        response = self.amity.print_unallocated()
        self.assertEqual(response, "\x1b[33mThis list is empty\x1b[0m")

    def test_prints_unallocated_to_screen(self):
        self.amity.add_person("The", "Man", "Fellow", "Y")
        self.amity.add_person("The", "guy", "Fellow", "N")
        self.amity.add_person("The", "dude", "Staff")
        person_identity = [person.the_id for person in self.amity.fellows]
        staff_identity = [person.the_id for person in self.amity.staff]
        response = self.amity.print_unallocated()
        expected = "\x1b[34mThe following people are unallocated: \n%s:- THE MAN (Fellow) ---> Not allocated with: Office and Living Space\n%s:- THE GUY (Fellow) ---> Not allocated with: Office and Living Space\n%s:- THE DUDE (Staff) ---> Not allocated with: Office\n\x1b[0m" % (
            person_identity[0], person_identity[1], staff_identity[0])
        self.assertEqual(response, expected)

    def test_prints_unallocated_to_file(self):
        self.amity.add_person("The", "Man", "Fellow", "Y")
        self.amity.add_person("The", "guy", "Fellow", "N")
        self.amity.add_person("The", "dude", "Staff")
        response = self.amity.print_unallocated("testingme")
        self.assertEqual(
            response, "\x1b[36mData has been successfully saved to testingme.txt\x1b[0m")

    def test_dbfile_created(self):
        self.amity.save_state("file.db")
        self.assertTrue(os.path.exists("file.db"))

    def test_save_state(self):
        response = self.amity.save_state("my_db")
        self.assertEqual(
            response, "\x1b[36mData saved to my_db.db successfully!\x1b[0m")

    def test_load_state_for_nonexisting_file(self):
        response = self.amity.load_state("lolik")
        self.assertEqual(
            response, "\x1b[31mThe database does not exist!\x1b[0m")

    def test_wrong_format_db(self):
        response = self.amity.load_state("mydb")
        self.assertEqual(response, "\x1b[31mThis file is in wrong format\x1b[0m")

    def test_load_state_successful(self):
        response = self.amity.load_state("amity")
        self.assertEqual(response, "\x1b[36mData loaded successfully!\x1b[0m")

    def test_for_nonexistant_room_delete(self):
        response = self.amity.remove_room("lagos")
        self.assertEqual(response, "\x1b[31mRoom: LAGOS not in Amity\x1b[0m")

    def test_room_deleted_successfully(self):
        self.amity.create_room("o", "Tanga")
        response = self.amity.remove_room("tanga")
        self.assertEqual(response, "\x1b[35mRoom: TANGA has been deleted from Amity!\x1b[0m")

    def test_string_input(self):
        self.amity.add_person("Jeff", "Kungu", "Staff")
        response = self.amity.remove_person("Jeff Kungu")
        self.assertEqual(response, "\x1b[33mUse Id's for identifying a person, NOT name\x1b[0m")

    def test_removes_person(self):
        self.amity.add_person("Eugene", "Omar", "Staff")
        person_identity = [person.the_id for person in self.amity.staff][0]
        response = self.amity.remove_person(person_identity)
        self.assertEqual(response, "\x1b[35mEUGENE OMAR has been successfully deleted from Amity.\x1b[0m")

    def test_wrong_id_remove(self):
        response = self.amity.remove_person(12345)
        self.assertEqual(response, "\x1b[31mThis person does not exist\x1b[0m")

if __name__ == '__main__':
    unittest.main()
