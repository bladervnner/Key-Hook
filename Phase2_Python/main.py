import sys
from pprint import pprint
from datetime import datetime

from db_connection import Session, engine
from orm_base import metadata
import logging
from sqlalchemy import MetaData

from access import Hooks, Keys, Permissions
from manufacture import Buildings, Rooms, Doors, DoorNames
from issue import Issues, Requests, Returns, Losses, Employees


# functions to print rooms, hooks, and employees in the database using querie
def printRooms():
    print("Here is a list of the rooms:")
    records = sess.query(Rooms).all()
    for record in records:
        pprint(record.__dict__)

def printHooks():
    print("Here is a list of the hooks:")
    records = sess.query(Hooks).all()
    for record in records:
        pprint(record.__dict__)

def printEmployees():
    print("Here is a list of employeeIDs:")
    records = sess.query(Employees).all()
    for record in records:
        pprint(record.__dict__)


# applications's menu for easy access each loop
def printMenu():
    print("Menu Options")
    print("\ta:Create key")
    print("\tb:Request access to a given room by a given employee.")
    print("\tc:Capture the issue of a key to an employee")
    print("\td:Capture losing a key")
    print("\te:Report out all the rooms that an employee can enter, given the keys that he/she already has.")
    print("\tf:Delete a key.")
    print("\tg:Delete an employee.")
    print("\th:Add a new door that can be opened by an existing hook.")
    print("\ti:Update an access request to move it to a new employee.")
    print("\tj:Report out all the employees who can get into a room.")
    print("\tq: Quit Menu")

if __name__ == '__main__':
    
    # establish connection with database
    metadata_object = MetaData()
    metadata_object.reflect(engine, schema="Hook_Project")

    metadata.create_all(bind=engine)

    with Session() as sess:
        while True:
            printMenu()
            choice = input("Select an option from menu: \n")
            #create a key
            if choice == 'a':
                #Printing hooks and receiving hook inputs
                printHooks()
                print("Creating a key\n")
                """ Error handling, with session rollback included if Exception is triggered"""
                try:
                    hookInp = input("Enter the hook serial number")
                    hook: Hooks = Hooks(serial_number=int(hookInp))
                    sess.commit()
                except Exception as ex:
                    print("Invalid Input")
                    sess.rollback()
                    pprint(ex)

                keys = sess.query(Keys).all()

                try:
                    key: Keys = Keys(hook=hook, key_serial_number=keys[len(keys)-1].key_serial_number+1)
                    sess.add(key)
                    sess.commit()
                except Exception as ex:
                    print("Invalid Input")
                    sess.rollback()
                    pprint(ex)

            elif choice == 'b':
                print("Request access to a given room by a given employee.\n")
                printEmployees()
                printRooms()
                idNum = int(input("Enter employee id"))
                roomNum = int(input("Enter room number"))
                building = str(input("Enter building name"))
                issues: [Issues] = sess.query(Issues).all()
                keys: [Keys] = sess.query(Keys).all()
                perm: [Permissions] = sess.query(Permissions).all()

                keyList = []
                hookList = []
                # permList = []

                for i in issues:
                    if (i.employee_id == idNum):
                        keyList += [i.key_serial_number]  # adds key serial number to list

                for k in keyList:
                    for h in keys:
                        if (h.key_serial_number == k):  #
                            hookList += [h.hook_serial_number]
                accessHook = False
                for i in hookList:
                    for p in perm:
                        if (p.building_name == building and p.room_number == roomNum and p.hook_serial_number == i):
                            print("Employee has access to " + str(p.building_name) + " "
                                  + str(p.room_number) + " " + str(p.door_name) + " already")
                            accessHook = p.hook_serial_number
                            break
                accessKey = []
                if (accessHook):
                    for k in keyList:
                        for key in keys:
                            if (accessHook == key.hook_serial_number):
                                accessKey += [key.key_serial_number]

                if (len(accessKey) < 1):
                    roomies: [Rooms] = sess.query(Rooms).all()
                    emps: [Employees] = sess.query(Employees).all()
                    temp1 = False
                    temp2 = False

                    for i in emps:
                        if (i.employee_id == idNum):
                            temp1 = i
                            break

                    for i in roomies:
                        if (i.building_name == building and i.number == roomNum):
                            temp2 = i
                            break

                    if (temp1 and temp2):
                        request: Requests = Requests(temp2, temp1, datetime.now())
                        sess.add(request)
                        try:
                            sess.commit()
                        except Exception as ex:
                            print("There was an error")
                            sess.rollback()
                            pprint(ex)
                    else:
                        print(
                            "Either that employee id does not exist or building name and building number are wrong")

                if (len(accessKey) > 0):
                    print("using key " + str(accessKey[0]))

            elif choice == 'c':
                print("Capture the issue of a key to an employee\n")
                #printing employees
                employees = sess.query(Employees).all()
                for e in employees:
                    pprint(e.__dict__)

                #receiving input
                empID = input("Enter an employee ID")

                #requests: list for all the requests that the employee made
                #requests2: list for all the requests that the employee made that have not been issued yet
                requests = sess.query(Requests).filter(Requests.employee_id == int(empID))
                requests2 = []

                #Nested for loops to search for the requests that have not been issued
                for r in requests:
                    found = False
                    issues = sess.query(Issues).filter(Issues.employee_id == int(empID))
                    for i in issues:
                        if (r.request_date == i.request_date):
                            found = True
                            break
                    if (found == False):
                        requests2.append(r)

                #keys2: list for the keys that can open the requested room
                keys2 = []

                #A lot of nested loops to search for the keys that can open the requested room
                for r in requests2:
                    permissions = sess.query(Permissions).filter(r.room_number == Permissions.room_number and
                                                                 r.building_name == Permissions.building_name)
                    for p in permissions:
                        hooks = sess.query(Hooks).filter(Hooks.serial_number == p.hook_serial_number)
                        for h in hooks:
                            keys = sess.query(Keys).filter(Keys.hook_serial_number == h.serial_number)
                            for k in keys:
                                found = False
                                if(k.key_serial_number == Issues.key_serial_number):
                                    found = True
                                    break
                                if(found == False):
                                    keys2.append(k)

                print('Here is a list of requests that have not been issued yet')

                #printing out the requests that have not been issued yet
                num = 0
                for record in requests2:
                    recordObject = {
                        'num ': num,
                        'employee_id': record.employee_id,
                        'room_number': record.room_number,
                        'building_name': record.building_name,
                        'request_date': record.request_date
                    }
                    pprint(recordObject)
                    num += 1

                reqInp = input('Enter num value next to request')

                #Recognizing the fact that there could be no available keys to open that room
                #Maybe add an error handlign here
                if(len(keys2) < 1):
                    print('no available keys for this request')

                #printing the keys that can be issued to the employee to open the room
                for record in keys2:
                    pprint(record.__dict__)

                keyInp = input('Enter key serial')

                #Searching for that key that has been selected
                key = False

                for record in keys2:
                    if(record.key_serial_number == int(keyInp)):
                        key = record

                issues = sess.query(Issues).all()

                #Creating an Issues instance
                issue: Issues = Issues(issue_id=len(issues)+1, request=requests2[int(reqInp)], key=key, issue_date=datetime.now())

                #adding and committing session
                sess.add(issue)
                sess.commit()

            elif choice == 'd':
                #P.S. Should we have a different input from the user other than the issueID,
                # maybe like a key_serial number instead?

                print("Capture losing a key\n")
                #printing all the current issues
                issues = sess.query(Issues).all()
                issues2 = []

                for i in issues:
                    Found = False
                    losses = sess.query(Losses).all()
                    for l in losses:
                        if (l.issue_id == i.issue_id):
                            Found = True
                            break
                    if (Found == False):
                        issues2.append(i)

                for record in issues2:
                    pprint(record.__dict__)

                issueIdInput = input("Enter issue ID of lost key")
                #Creating a Losses instance
                loss: Losses = Losses(issue_id=int(issueIdInput), loss_date=datetime.now())

                #adding and committing session
                sess.add(loss)
                try:
                    sess.commit()
                except Exception as ex:
                    print("There was an error")
                    sess.rollback()
                    pprint(ex)

            elif choice == 'e':
                print("Report out all the rooms that an employee can enter, "
                      "given the keys that he/she already has.\n")
                #printing employees
                printEmployees()

                #Reference lists
                issues: [Issues] = sess.query(Issues).all()
                keys: [Keys] = sess.query(Keys).all()
                perm: [Permissions] = sess.query(Permissions).all()


                keyList = []
                hookList = []
                idNum = int(input("Enter employee id: "))
                for i in issues:
                    if (i.employee_id == idNum):
                        keyList += [i.key_serial_number]  # adds key serial number to list

                for k in keyList:
                    for h in keys:
                        if (h.key_serial_number == k):
                            hookList += [h.hook_serial_number]
                for i in hookList:
                    for p in perm:
                        if (p.hook_serial_number == i):
                            print("Employee has access to " + str(p.building_name) + " "
                                  + str(p.room_number) + " " + str(p.door_name))

            elif choice == 'f':
                print("Delete a key.\n")
                print("Here is a list of the keys:")
                #printing keys
                keys = sess.query(Keys).all()
                for i in keys:
                    pprint(i.__dict__)
                keyInp = input("Enter the key serial")

                num = 0
                key = False

                #Searching for selected key
                for i in keys:
                    if(i.key_serial_number == int(keyInp)):
                        key = i
                        break
                    num += 1
                #Deleting all the children of that key (issues, returns, and losses)
                issues = sess.query(Issues).filter(key.key_serial_number == Issues.key_serial_number)
                for issue in issues:
                    returns = sess.query(Returns).filter(issue.issue_id == Returns.issue_id)
                    for r in returns:
                        sess.delete(r)
                    losses = sess.query(Losses).filter(issue.issue_id == Losses.issue_id)
                    for l in losses:
                        sess.delete(l)
                    sess.delete(issue)

                #Deleting the key and committing
                try:
                    sess.delete(keys[num])
                    sess.commit()
                except Exception as ex:
                    print("Invalid Input")
                    sess.rollback()
                    pprint(ex)

            elif choice == 'g':
                print("Delete an employee.\n")
                #printing employees
                print("Here is a list of the employeeIDs:")
                employees = sess.query(Employees).all()
                for employee in employees:
                    pprint(employee.__dict__)

                empInp = input("Enter the employeeID")

                #Searching for selected employee
                emp = False
                num = 0

                for e in employees:
                    if e.employee_id == int(empInp):
                        emp = e
                        break
                    num += 1

                #Deleting all children of the employee (requests, issues, returns, and losses)
                requests = sess.query(Requests).filter(Requests.employee_id == int(empInp))
                for request in requests:
                    issues = sess.query(Issues).filter(request.request_date == Issues.request_date)
                    for issue in issues:
                        returns = sess.query(Returns).filter(issue.issue_id == Returns.issue_id)
                        for r in returns:
                            sess.delete(r)
                        losses = sess.query(Losses).filter(issue.issue_id == Losses.issue_id)
                        for l in losses:
                            sess.delete(l)
                        sess.delete(issue)
                    sess.delete(request)

                #Deleteing the employee and comitting
                try:
                    sess.delete(employees[num])
                    sess.commit()
                except Exception as ex:
                    print("Invalid Input")
                    sess.rollback()
                    pprint(ex)

            elif choice == 'h':
                print("Add a new door that can be opened by an existing hook.\n")
                #printing hooks
                printHooks()

                hookInp = input('Enter a hook serial')

                #hook is a list of one object that contains the selected hook
                hook = sess.query(Hooks).filter(Hooks.serial_number == int(hookInp))

                #printing rooms
                printRooms()

                building = input('Enter building name')
                room = input('Enter room number')

                #doors is a list of one object that contains the doors from the selected room
                doors = sess.query(Doors).filter(Doors.room_number == int(room)
                                                 and Doors.building_name == building)

                #printing doors in the room
                for door in doors:
                    pprint(door.__dict__)

                #new doorName input
                doorInp = input("Select a door name that doesn't already exists in this room:"
                                "\nKeep in mind: Valid door names are: \'W\', \'S\', \'N\', \'E\'")

                rooms = sess.query(Rooms).filter(Rooms.number == int(room) and Rooms.building_name == building)

                dName = sess.query(DoorNames).filter(DoorNames.name == doorInp)

                #Creating, adding and comitting a new door
                door: Doors = Doors(room=rooms[0], doorName=dName[0])
                sess.add(door)
                sess.commit()

                #Creating, adding and comitting a new permission
                perm: Permissions = Permissions(hook=hook[0], door=door)
                sess.add(perm)
                sess.commit()

            elif choice == 'i':
                print("Update an access request to move it to a new employee.\n")
                #printing current requests
                print("Here is a list of the requests:")
                records = sess.query(Requests).all()
                num = 0
                for record in records:
                    recordObject = {
                        'num ': num,
                        'employee_id': record.employee_id,
                        'room_number': record.room_number,
                        'building_name': record.building_name,
                        'request_date': record.request_date
                    }
                    pprint(recordObject)
                    num += 1

                reqInp = input('Enter the num value next to the request')

                #printing employees
                printEmployees()

                #new employeeID
                empInp = input("Enter an employeeID")

                # updating the request's employee_id
                records[int(reqInp)].employee_id = int(empInp)

                #Checking if the request has children
                issues = records[int(reqInp)].issues_list

                #updating all the children's new employee_id
                for issue in issues:
                    issue.employee_id = int(empInp)
                    sess.commit()

                #committing
                sess.commit()

            elif choice == 'j':
                print("Report out all the employees who can get into a room.\n")
                #printing employees and rooms
                printEmployees()
                printRooms()

                building = str(input("Enter building name"))
                roomNum = int(input("Enter room number"))

                #A list of Requests for the selected room
                requests: [Requests] = sess.query(Requests).filter(Requests.building_name == building
                                                                   and Requests.room == roomNum)

                #a list of all employees
                emps: [Employees] = sess.query(Employees).all()

                #list of employees that can access the room
                access = []

                #Searching for the employees that can access the room
                for r in requests:
                    issues = sess.query(Issues).filter(Issues.request_date == r.request_date)
                    for i in issues:
                        access += [i.employee_id]

                #Printing out the employees
                for e in access:
                    for i in emps:
                        if (i.employee_id == e):
                            print(str(i.name) + " has access to " + str(building) + " " + str(roomNum))

                # sends a message that the room cannot be accessed by anyone
                if (len(access) < 1):
                    print("Looks like no one has access to that room")

            elif choice == 'q':
                sys.exit()
                print("Exiting normally.")
            else:
                print("invalid choice\n")

