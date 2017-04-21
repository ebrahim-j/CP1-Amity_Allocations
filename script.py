from amity import Amity
amity = Amity()

# amity.load_state("test")
# all_rooms = amity.offices + amity.l_spaces
# all_persons = amity.staff + amity.fellows
# print([room.room_name for room in all_rooms])
# print([person.the_name for person in all_persons])


# amity.create_room("o", "oculus")
amity.create_room("l", "Homabay")
# # print(amity.load_people("text.txt"))
# # print(amity.create_room("l", "Homabay"))
# # print(amity.create_room("l", "Surat"))
# # amity.create_room("o", "Rome")
# amity.add_person("Faith", "fellow", "Y")
print(amity.add_person("Bernard","Mulobi", "fellow", "Y"))
# print(amity.add_person("Ahmed", "fellow", "Y"))
amity.create_room("l", "Rome")
# print(amity.print_room("Homabay"))
# print(amity.print_room("Rome"))
print(amity.reallocate_person("Bernard Mulobi", "Roe"))
# print(amity.print_room("Homabay"))
# print(amity.print_room("Rome"))
# # amity.add_person("Alex", "staff", "Y")
# # amity.add_person("Paul", "fellow", "Y")
# # amity.add_person("Millicent", "staff", "N")
# # amity.add_person("Ahmed", "fellow", "N")


# print(amity.print_unallocated())
# print(amity.print_allocations())
# amity.print_room("Surat")

# # amity.save_state("test1")
print(amity.load_people("tasfasdf.txt"))