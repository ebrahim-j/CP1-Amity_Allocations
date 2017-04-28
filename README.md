# CP1-Amity_Allocations
This model's a room allocation system for one of Andela’s facilities called Amity.
## Introduction

**CP1-Amity_Allocations** is a CLI app that handles room allocation for Fellow and Staff at one of Andela's facilities Amity. **Staff** can only be allocated office space while **Fellows** are allocated office space and living space if they choose so.


* Link to demo video: (https://asciinema.org/a/0g7ynj7d55g36z3bm390vn6k0)


## Installation and setup
Clone the repo into a folder of your choice on your 'terminal'
```
git clone https://github.com/ebrahim-j/CP1-Amity_Allocations/tree/develop
```
Create a virtual environment.
```
virtualenv venv
```
Navigate to the project folder
```
cd amity
```
Activate your virtual environment
```
source venv/bin/activate
```
alternatively, if you have a virtualenvwrapper:
```
workon venv
```
Install the required packages
```
pip install -r requirements.txt
```

## Launching the application
```
python app.py
```
You are good to go!
Interact with the program by running the following commands

## Commands to run:

* To create a new office or living space(Multiple rooms can be created in line) run ```create_room <room_type> <room_names>...```

* To add a new staff or fellow run```add_person <person_name> <role> [<wants_accomodation>]```.
 For fellows who want accomodation specify the optional 'y' parameter

* To view all members in any room run ```print_room <room_name>```

* To view all allocations i.e. every room and their occupants run ```print_allocations [<filename>]``` 
 specifying a filename saves the records in a ```.txt``` file

* To view all unallocated persons run ```print_unallocated [<filename>]``` 
 specifying a filename saves the records in a ```.txt``` file

* ```load_people <filename>``` loads people from an existing ```.txt``` file

* ```reallocate_person <identifier> <new_room_name>``` reallocates a person from their current room to the given room

* ```save_state [<database_name>]``` saves the current state of the application to a database. Specifying the database_name saves the data to named database file

* ```load_state <database_name>``` loads data from an exisitng SQL database

## Testing
* Run ```nosetests ```

 *  To view test coverage statistics, run the following command;
 	```nosetests --with-coverage```
