import pymongo

import sys
from pprint import pprint
from datetime import datetime

from Utilities import Utilities
from validators import validate

if __name__ == '__main__':

    def printRooms():
        rooms = db.rooms
        for room in rooms.find({}, {"_id": 0}):
            print(room)


    def printHooks():
        hooks = db.hooks
        for hook in hooks.find({}, {"_id": 0}):
            print(hook)


    def printEmployees():
        employees = db.employees
        for employee in employees.find({}, {"_id": 0}):
            print(employee)


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


    db = Utilities.startup()

    # setting up the buildings collection
    buildings = db.buildings
    buildings.create_index([("name", pymongo.ASCENDING)], unique=True)

    # setting up the rooms collection
    rooms = db.rooms
    rooms.create_index([("building_name", pymongo.ASCENDING), ("number", pymongo.ASCENDING)], unique=True)

    # setting up door_names collection
    door_names = db.door_names
    door_names.create_index([("name", pymongo.ASCENDING)], unique=True)

    # setting up doors collection
    doors = db.doors
    doors.create_index([("building_name", pymongo.ASCENDING), ("room_number", pymongo.ASCENDING),
                        ("name", pymongo.ASCENDING)], unique=True)

    # setting up employees collection
    employees = db.employees
    employees.create_index([("employee_id", pymongo.ASCENDING)], unique=True)

    # setting up hooks collection
    hooks = db.hooks
    hooks.create_index([("serial_number", pymongo.ASCENDING)], unique=True)

    # setting up keys collection
    keys = db.keys
    keys.create_index([("key_serial_number", pymongo.ASCENDING)], unique=True)

    # setting up permissions collection
    permissions = db.permissions
    permissions.create_index([("hook_serial_number", pymongo.ASCENDING), ("room_number", pymongo.ASCENDING),
                              ("building_name", pymongo.ASCENDING), ("door_name", pymongo.ASCENDING)],
                             unique=True)

    # setting up requests collection
    requests = db.requests
    requests.create_index([("employee_id", pymongo.ASCENDING), ("room_number", pymongo.ASCENDING),
                           ("building_name", pymongo.ASCENDING), ("request_date", pymongo.ASCENDING)],
                          unique=True)

    # setting up issues collection
    issues = db.issues
    issues.create_index([("issue_id", pymongo.ASCENDING)], unique=True)

    # setting up returns collection
    returns = db.returns
    returns.create_index([("issue_id", pymongo.ASCENDING)], unique=True)

    # setting up losses collection
    losses = db.losses
    losses.create_index([("issue_id", pymongo.ASCENDING)], unique=True)

    # function to implement all the validators
    validate()

    while True:
        printMenu()
        choice = input("Select an option from menu: \n")
        if choice == 'a':
            # Weak approach, we should use serial number instead, just don't know how yet
            keysList = list(keys.find({}))
            for i in range(len(keysList)):
                if i == len(keysList) - 1:
                    lastSN = keysList[i]['key_serial_number']

            print("Creating a key\n")
            printHooks()
            while True:
                created = False
                try:
                    hookInp = int(input("Enter the hook serial number:"))
                    for h in list(hooks.find({})):
                        if hookInp == h['serial_number']:
                            created = True
                            keys.insert_one({"key_serial_number": lastSN + 1, "hook_serial_number": hookInp, })
                            print("Key added successfully!")
                            break
                    if not created:
                        print("hook does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid hook serial number.\n")

        elif choice == 'b':
            print("Requesting access to a given room by a given employee.\n")

            printEmployees()

            while True:
                found = False
                try:
                    idNum = int(input("Enter employee id: "))
                    for i in list(employees.find({})):
                        if idNum == i['employee_id']:
                            found = True
                            break
                    if not found:
                        print("employee does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid employee_id.\n")

            printRooms()
            while True:
                found = False
                try:
                    building = str(input("Enter building name: "))
                    roomNum = int(input("Enter room number: "))
                    for r in list(rooms.find({})):
                        if roomNum == r['number'] and building == r['building_name']:
                            found = True
                            break
                    if not found:
                        print("room does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid building and room number.\n")

            # setting up lists
            issuesList = issues.find({})
            keysList = keys.find({}, {"_id": 0, "key_serial_number": 1})
            permList = permissions.find({})

            usedKeys = []
            usedHooks = []
            usedKeys2 = []

            for i in issues.find({"employee_id": idNum}, {"_id": 0, "key_serial_number": 1}):
                if (len(list(i)) > 0):
                    usedKeys += [i]
                    usedKeys2 += [i['key_serial_number']]

            for k in usedKeys2:
                for key in keysList:
                    if key['key_serial_number'] == k:
                        hook = keys.find_one({"key_serial_number": k})['hook_serial_number']
                        usedHooks.append(hook)

            accessHook = False

            for h in usedHooks:
                perms = permissions.find({"building_name": building, "room_number": roomNum,
                                          "hook_serial_number": h})
                if len(list(perms)) > 0:
                    print(f"Employee already has access to {building} {roomNum}")
                    accessHook = h
                    break

            accessKey = []
            if accessHook:
                for k in usedKeys2:
                    hook = keys.find_one({"key_serial_number": k})['hook_serial_number']
                    if accessHook == hook:
                        accessKey.append(k)

            if len(accessKey) < 1:
                try:
                    requests.insert_one({"employee_id": idNum, "room_number": roomNum,
                                         "building_name": building, "request_date": datetime.now()})
                    print("Request made successfully!\n")
                except Exception as ex:
                    print("Request not successful\n")
                    pprint(ex)

        elif choice == 'c':

            print("Capturing the issue of a key to an employee\n")

            # printing employees
            printEmployees()

            # receiving input
            while True:
                found = False
                try:
                    empID = int(input("Enter an employee ID: "))
                    for i in list(employees.find({})):
                        if empID == i['employee_id']:
                            found = True
                            break
                    if not found:
                        print("employee does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid employee_id.\n")

            # requests: list for all the requests that the employee made
            # requests2: list for all the requests that the employee made that have not been issued yet
            requestsList = requests.find({"employee_id": empID}, {"_id": 0, "request_date": 1})
            requests2 = []

            # Nested for loops to search for the requests that have not been issued
            for r in requestsList:
                found = False
                issuesList = issues.find({"employee_id": empID}, {"_id": 0, "request_date": 1})
                for i in issuesList:
                    if r['request_date'] == i['request_date']:
                        found = True
                        break
                req = requests.find_one({"request_date": r['request_date']}, {"_id": 0})
                if not found:
                    requests2.append(req)

            availableKeys = []

            for r in list(requests2):
                perms = permissions.find({"room_number": r['room_number'], "building_name": r['building_name']})
                for p in list(perms):
                    hooksList = hooks.find({"serial_number": p['hook_serial_number']})
                    for h in list(hooksList):
                        keysList = keys.find({"hook_serial_number": h['serial_number']})
                        for k in list(keysList):
                            found = False
                            issuesList = issues.find({"key_serial_number": k['key_serial_number']})
                            if len(list(issuesList)) > 0:
                                found = True
                            if not found:
                                availableKeys.append(k)

            if len(list(requests2)) < 1:
                try:
                    x = 1 / 'hi'
                except Exception as ex:
                    print("Please request the room first using option \'b\'!\n")
            else:
                print("Here is a list of the requests that have not been issued to the employee: ")
                for r in range(len(list(requests2))):
                    print(f'num : {r} {list(requests2)[r]}\n')

                while True:
                    found = False
                    try:
                        reqInp = int(input("Enter the num value next to the request: "))
                        for i in range(len(list(requests2))):
                            if reqInp == i:
                                found = True
                                break
                        if not found:
                            print("request does not exist\n")
                        else:
                            req = list(requests2)[reqInp]
                            break
                    except Exception as ex:
                        print("Invalid Input. Please select a valid num value.\n")

                if len(availableKeys) < 1:
                    print("There were no available keys for that room, but we just made a new one for you!\n")

                    hook = permissions.find_one({"building_name": req['building_name'],
                                                 "room_number": req['room_number']})['hook_serial_number']
                    keysList = keys.find({})
                    keyS = len(list(keysList)) + 1
                    keys.insert_one({"hook_serial_number": hook, "key_serial_number": len(list(keysList)) + 1})
                else:
                    print("Here is a list of keys available that can open the room requested: ")
                    for k in availableKeys:
                        print(k['key_serial_number'])

                    while True:
                        found = False
                        try:
                            keyS = int(input("Enter the key serial number: "))
                            for k in list(keys.find({})):
                                if keyS == k['key_serial_number']:
                                    found = True
                                    break
                            if not found:
                                print("key does not exist\n")
                            else:
                                break
                        except Exception as ex:
                            print("Invalid Input. Please select a valid key serial.\n")

                issuesList = list(issues.find({}))
                for i in range(len(issuesList)):
                    if i == len(issuesList) - 1:
                        lastID = issuesList[i]['issue_id']

                try:
                    issues.insert_one({"issue_id": lastID + 1,
                                       "employee_id": empID,
                                       "room_number": req['room_number'],
                                       "building_name": req['building_name'],
                                       "request_date": req['request_date'],
                                       "key_serial_number": keyS,
                                       "issue_date": datetime.now()})
                    print("Issue was a success!\n")
                except:
                    print("Issue not successful\n")

        elif choice == 'd':
            print("Capturing losing a key\n")
            issuesList = issues.find({}, {"_id": 0})
            issuesList2 = []

            lossesList = list(losses.find({}))
            returnsList = list(returns.find({}))

            for i in list(issuesList):
                lost = False
                for l in lossesList:
                    if i['issue_id'] == l['issue_id']:
                        lost = True
                        # break
                for r in returnsList:
                    if i['issue_id'] == r['issue_id']:
                        lost = True
                        # break
                if not lost:
                    issuesList2.append(i)

            print("Here is a list of all issues that are not lost/returned yet:")
            for i in issuesList2:
                print(i)

            while True:
                found = False
                try:
                    iid = int(input("Enter issue_id: "))
                    for i in issuesList2:
                        if iid == i['issue_id']:
                            found = True
                            break
                    if not found:
                        print("issue not on the list\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid issue id.\n")

            try:
                losses.insert_one({"issue_id": iid, "loss_date": datetime.now()})
                print("Loss was reported successfully!\n")
            except:
                print("Loss was not reported!\n")


        elif choice == 'e':
            print("Reporting out all the rooms that an employee can enter\n")

            print("Here is a list of the employees!\n")
            printEmployees()

            while True:
                found = False
                try:
                    idNum = int(input("Enter the employee ID: "))
                    for e in list(employees.find({})):
                        if idNum == e['employee_id']:
                            found = True
                            break
                    if not found:
                        print("employee does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid employee id.\n")

            issuesList = issues.find({})
            keysList = keys.find({})
            permList = permissions.find({})

            empKeys = []
            hooksList = []

            for i in list(issuesList):
                if i['employee_id'] == idNum:
                    empKeys.append(i['key_serial_number'])

            for eK in empKeys:
                for k in list(keysList):
                    if k['key_serial_number'] == eK:
                        hooksList.append(k['hook_serial_number'])

            roomiesB = []

            roomiesR = []

            roomies = []

            for h in hooksList:

                for p in list(permList):

                    if p['hook_serial_number'] == h:
                        roomiesB.append(rooms.find_one({"building_name": p['building_name'],

                                                        "number": p['room_number']})['building_name'])

                        roomiesR.append(rooms.find_one({"building_name": p['building_name'],

                                                        "number": p['room_number']})['number'])

                        roomies.append(rooms.find_one({"building_name": p['building_name'],

                                                       "number": p['room_number']}, {"_id": 0}))

                        # Order by building, then room

                        # remove duplicates

                        # print(f"Employee has access to {p['building_name']} {p['room_number']}.\n")

            for room, num in enumerate(roomiesB):
                roomiesB[room] = "{} {}".format(str(num), roomiesR[room])
            roomiesB.sort()
            res = [*set(roomiesB)]
            res.sort()
            print(res)

            #print(roomiesB)  ## if you put id: 2 shows you the list before removing duplicate

        elif choice == 'f':
            print("Delete a key.\n")
            print("Here is a list of the keys:")

            issuesList = list(issues.find({}, {"_id": 0}))
            keysList = list(keys.find({}, {"_id": 0, "hook_serial_number": 0}))

            for k in keysList:
                print(k)

            while True:
                found = False
                try:
                    keyInp = input("Enter the key serial: ")
                    for k in list(keys.find({})):
                        if int(keyInp) == k['key_serial_number']:
                            found = True
                            break
                    if not found:
                        print("key does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid key serial.\n")

            num = 0
            key = False
            issue = False
            # Searching for selected key
            for dic in keysList:
                if dic['key_serial_number'] == int(keyInp):
                    key = dic
                    break
                num += 1
            for dic in issuesList:
                if dic['key_serial_number'] == int(keyInp):
                    issue = dic['issue_id']
            if key and issue:
                print(f"key is referenced in issue {issue} and cannot be deleted")

            elif (key):
                keys.delete_one(key)  # I did not want to mess with your data so I commented out,
                print("Key deleted successfully!\n")
            else:
                print("key not deleted\n")

        elif choice == 'g':
            print("Deleting an employee.\n")
            print("Here is a list of the employeeIDs:\n")

            printEmployees()

            while True:
                found = False
                try:
                    empInp = input("Enter an employeeID: ")
                    for e in list(employees.find({})):
                        if int(empInp) == e['employee_id']:
                            found = True
                            break
                    if not found:
                        print("employee does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid employee id.\n")

            emp = False
            num = 0

            employeesList = list(employees.find({}))

            for e in employeesList:
                for i in e:
                    if e['employee_id'] == int(empInp):
                        emp = e
                        break
                    num += 1

            # Deleting all children of the employee (requests, issues, returns, and losses)
            requestsFilter = requests.find({"employee_id": int(empInp)})
            for request in requestsFilter:
                issuesFilter = issues.find({'request_date': request['request_date']})
                for issue in issuesFilter:
                    returnsFilter = returns.find({'issue_id': issue['issue_id']})
                    for r in returnsFilter:
                        returns.delete_one(r)
                    lossesFilter = losses.find({'issue_id': issue['issue_id']})
                    for l in lossesFilter:
                        losses.delete_one(l)
                    issues.delete_one(issue)
                requests.delete_one(request)

            if (emp):
                employees.delete_one(emp)
                print("Employee deleted successfully!\n")
            else:
                print("Employee not found.\n")


        elif choice == 'h':
            print("Adding a new door that can be opened by an existing hook.\n")
            # printing hooks
            printHooks()

            while True:
                found = False
                try:
                    hookInp = input('Enter hook serial: ')
                    for h in list(hooks.find({})):
                        if int(hookInp) == h['serial_number']:
                            found = True
                            break
                    if not found:
                        print("hook does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid hook serial.\n")

            hook = hooks.find({'serial_number': int(hookInp)})

            printRooms()

            while True:
                found = False
                try:
                    building = str(input("Enter building name: "))
                    room = int(input("Enter room number: "))
                    for r in list(rooms.find({})):
                        if room == r['number'] and building == r['building_name']:
                            found = True
                            break
                    if not found:
                        print("room does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid building and room number.\n")

            doorList = list(doors.find({'room_number': int(room), 'building_name': building}, {'_id': 0}))

            for d in doorList:
                pprint(d)

            while True:
                valid = False
                found = False
                try:
                    doorInp = input("Select a door name that doesn't already exists in this room:"
                                    "\nKeep in mind: Valid door names are: ('W', 'S', 'N', 'E') ")
                    for d in list(door_names.find({})):
                        if doorInp == d['name']:
                            valid = True
                        for d2 in doorList:
                            if doorInp == d2['name']:
                                found = True
                                break
                    if found:
                        print("door already exists\n")
                    elif not found and valid:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid door as instructed.\n")

            roomList = (rooms.find_one({'building_name': building, 'number': int(room)}))

            dName = (door_names.find_one({'name': doorInp}))

            try:
                door = doors.insert_one({'name': dName['name'], "room_number": roomList['number'],
                                         'building_name': roomList['building_name']})
                print("Door has been added successfully!\n")
            except Exception as ex:
                print("door not added\n")
                pprint(ex)
            try:
                permissions.insert_one({"hook_serial_number": int(hookInp), "room_number": int(roomList['number']),
                                        'building_name': roomList['building_name'], 'door_name': dName['name']})
                print("Permission has been added successfully!\n")
            except Exception as ex:
                print("Permission not added.\n")
                pprint(ex)

        elif choice == 'i':
            print("Updating an access request to move it to a new employee.\n")

            printEmployees()
            while True:
                found = False
                try:
                    oldEmp = int(input("Enter the old employeeID you want to move the request from: "))
                    for e in list(employees.find({})):
                        if oldEmp == e['employee_id']:
                            found = True
                            break
                    if not found:
                        print("employee does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid employee id.\n")

            print("Here is a list of the requests:")

            requestsList = list(requests.find({"employee_id": oldEmp}, {"_id": 0}))

            if len(requestsList) < 1:
                raise Exception("Employee has no requests.")

            for r in range(len(requestsList)):
                print(f'num : {r} {requestsList[r]}\n')

            while True:
                found = False
                try:
                    reqInp = int(input("Enter the num value next to the request: "))
                    for i in range(len(requestsList)):
                        if reqInp == i:
                            found = True
                            break
                    if not found:
                        print("request does not exist\n")
                    else:
                        req = requestsList[reqInp]
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid num value.\n")
            print()

            printEmployees()

            while True:
                found = False
                try:
                    newEmp = int(input("Enter the new employeeID you want to move the request to: "))
                    for e in list(employees.find({})):
                        if newEmp == e['employee_id'] and newEmp != oldEmp:
                            found = True
                            break
                    if not found:
                        print("employee does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid employee id "
                          "(make sure you are not selecting the same old employee).\n")

            # updating the request's employee_id
            oldReq = {"request_date": requestsList[reqInp]['request_date']}
            newValue = {"$set": {"employee_id": newEmp}}

            try:
                requests.update_one(oldReq, newValue)
                print("Request updated successfully!")
            except:
                print("Request was not updated.")

            # updating all the children's new employee_id
            for issue in list(issues.find({})):
                issues.update_one(oldReq, newValue)

        elif choice == 'j':
            print("Report out all the employees who can get into a room.\n")

            printRooms()
            while True:
                found = False
                try:
                    building = str(input("Enter building name: "))
                    roomNum = int(input("Enter room number: "))
                    for r in list(rooms.find({})):
                        if roomNum == r['number'] and building == r['building_name']:
                            found = True
                            break
                    if not found:
                        print("room does not exist\n")
                    else:
                        break
                except Exception as ex:
                    print("Invalid Input. Please select a valid building and room number.\n")

            # A list of issues for the selected room
            # issuesList = list(issues.find({"room_number": roomNum}, {"building_name": building}))
            issuesList = list(issues.find({"room_number": roomNum, "building_name": building}))

            # A list of all employees that have access
            empsList = []

            if len(issuesList) < 1:
                print("No employee has access to such room")
            else:
                for dic in issuesList:
                    # empsList += [employees.find_one({"employee_id": dic['employee_id']})[
                    # 'name']]  # no need for this only for test purposes
                    # print(employees.find_one({"employee_id": dic['employee_id']})['name'], "has access to ", building, roomNum)
                    if (len(issuesList) == 1 or dic == issuesList[0]):
                        print(employees.find_one({"employee_id": dic['employee_id']})['name'], end="")
                    else:
                        print(", ", employees.find_one({"employee_id": dic['employee_id']})['name'], end="")
                print()

        elif choice == 'q':
            print("Exiting normally.")
            sys.exit()
        else:
            print("invalid choice\n")
