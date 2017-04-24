"""
AMITY.
Usage:
    amity create_room <room_type> <room_name>...
    amity add_person <first_name> <second_name> <FELLOW|STAFF> [wants_accommodation]
    amity reallocate_person <person_identifier> <new_room_name>
    amity load_people
    amity get_everyone
    amity print_allocations [-o]
    amity print_unallocated [-o]
    amity print_room <room_name>
    amity save_state [--db]
    amity load_state <sqlite_database>
    amity (-i | --interactive)
    amity (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from amity import Amity
from pyfiglet import figlet_format
from termcolor import cprint


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

def launch():
	cprint(figlet_format('AMITY', font='doom'), 'cyan', 
		attrs=['blink'])
	print("Welcome to the AMITY." + 
		"Here is a list of commands for your use " + 
		"Type 'help' anytime to access available commands")
	cprint(__doc__, 'blue')

class MyInteractive (cmd.Cmd):

    launch()

    prompt = '(Amity...) '
    file = None

    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        '''Instantiates a living space or office based on prefix
            Usage: create_room <room_type> <room_name>...'''

        name = arg['<room_name>']
        room_type = arg['<room_type>']

        for room in name:
            try:
                print(self.amity.create_room(room_type, room))
            except:
                print("Something went wrong.")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <second_name> <role> [<wants_accomodation>]"""

        fname = arg["<first_name>"]
        lname = arg["<second_name>"]
        role = arg["<role>"]
        wants_accommodation = arg["<wants_accomodation>"]

        print(self.amity.add_person(fname, lname, role, wants_accommodation))

    @docopt_cmd
    def do_reallocate_person(self, arg):
		"""Usage: reallocate_person <person_identifier> <new_room_name>"""

		identifier = arg["<person_identifier>"]
		new_room = arg["<new_room_name>"]

		print(self.amity.reallocate_person(int(identifier), new_room))

    @docopt_cmd
    def do_get_everyone(self, arg):
        """ Usage: get_everyone"""

        print(self.amity.get_everyone())


    @docopt_cmd
    def do_load_people(self, arg):
        """ Usage: load_people """

        print(self.amity.load_people())

    @docopt_cmd
    def do_print_allocations(self, arg):
        """ Usage: print_allocations [<--o>] """

        if arg['<--o>']:
            filename = arg['<--o>']
        else:
            filename = None


        print(self.amity.print_allocations(filename))


    @docopt_cmd
    def do_print_unallocated(self, arg):
        """ Usage: print_unallocated [<--o>] """

        if arg['<--o>']:
            filename = arg['<--o>']
        else:
            filename = None


        print(self.amity.print_unallocated(filename))

    @docopt_cmd
    def do_print_room(self, arg):
        """ Usage: print_rooms <room_name> """

        room_name = arg['<room_name>']

        print(self.amity.print_room(room_name))

    @docopt_cmd
    def do_save_state(self, arg):
        """ Usage: save_state [<--db>] """

        if arg['<--db>']:
            dbname = arg['<--db>']
        else:
            dbname = None

        print(self.amity.save_state(dbname))

    @docopt_cmd
    def do_load_state(self, arg):
        """ Usage: load_state <sqlite_database> """

        dbname = arg['<sqlite_database>']

        print(self.amity.load_state(dbname))

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()
