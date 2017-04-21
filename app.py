"""
AMITY.
Usage:
    class_attendance_register add_class <name>
    class_attendance_register remove_class <class_id>
    class_attendance_register log_in <class_id>
    class_attendance_register log_out <class_id>
    class_attendance_register list_classes
    class_attendance_register add_student <name>
    class_attendance_register remove_student <student_id>
    class_attendance_register check_in <student_id> <class_id>
    class_attendance_register check_out <student_id> <class_id> <reason>
    class_attendance_register list_students
    class_attendance_register (-i | --interactive)
    class_attendance_register (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from random import randint
import time
from Klass import Klass
from Student import Student
from Reason import Reason
import sqlite3

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


class MyInteractive (cmd.Cmd):
    intro = 'Welcome to my interactive program!' \
        + ' (type help for a list of commands.)'
    prompt = '(main) '
    file = None

    @docopt_cmd
    def do_add_class(self, arg):
        """Adds Class object to the database
			Usage: add_class <name>"""
        name = arg['<name>']
        Klass.add_class(name)

    @docopt_cmd
    def do_remove_class(self, arg):
        """Deletes class object from the database
			Usage: remove_class <class_id>"""
        class_id = arg['<class_id>']
			
        Klass.remove_class(class_id)

    @docopt_cmd
    def do_log_in(self, arg):
        """Logs in a class session
			Usage: log_in <class_id>"""
        class_id = arg['<class_id>']
        Klass.log_in(class_id)

    @docopt_cmd
    def do_log_out(self, arg):
        """Logs out a class session
			Usage: log_out <class_id>"""
        class_id = arg['<class_id>']
        Klass.log_out(class_id)

    @docopt_cmd
    def do_list_classes(self, arg):
        """Lists all the classes, whether in progress or not and the count of students in class
			Usage: list_classes"""

        Klass.list_classes()


    @docopt_cmd
    def do_add_student(self, arg):
        """Adds a student to the database
			Usage: add_student <name>"""
        name = arg['<name>']
        Student.add_student(name)

    @docopt_cmd
    def do_remove_student(self, arg):
        """Deletes a students from the database
			Usage: remove_student <student_id>"""
        student_id = arg['<student_id>']
        Student.remove_student(student_id)

    @docopt_cmd
    def do_check_in(self, arg):
        """ Checks a student into a class session
			Usage: check_in <student_id> <class_id>"""
        student_id = arg['<student_id>']
        class_id = arg['<class_id>']
        Student.checkIn(student_id, class_id)
		
    @docopt_cmd
    def do_check_out(self, arg):
        """Checks a student out of a class session 
			Usage: check_out <student_id> <class_id> <reason>"""
        student_id = arg['<student_id>']
        class_id = arg['<class_id>']
        reason = arg['<reason>']
        Reason.checkOut(student_id, class_id, reason)
		
    @docopt_cmd
    def do_list_students(self, arg):
        """Lists all the students and whether they are in class or not
			Usage: list_students"""

        Student.list_students()




    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()