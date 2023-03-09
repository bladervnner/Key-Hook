## Procedure Phase 1
1. UML model all business rules from business rules (seperate file)
2. For each of the business rules that cannot be implemented by the way the database is structured, write out pseudo code how those business rules will be implemented using Python code.
3. Once UML model (seperate file) has been completed, the next step is to build an ERD diagram. We will not implement tables for the ERD diagram. Instead, SQLAlchemy will build the tables for us.
3. Once UML model (seperate file) has been completed, the next step is to build an ERD diagram. We will not implement tables for the ERD diagram. Instead, SQLAlchemy will build the tables.

# Description Phase 2
Using SQLAlchemy to access a back-end database in PostgreSQL that is structured according to the phase 1 design
The goal of this phase is to demonstrate the use of SQLAlchemy in a console application. Application uses a hybrid approach to populate some of the tables. Insert, Update, and Delete data are achieved using SQLAlchemy. The code design handles any data input from the user. 
## Procedure Phase 2
Used ERD from phase 1 and executed the CREATE TABLE statements that it produces. Wrote insert statements to populate: 
 * Employees, Buildings, rooms, doors, hooks, and any junction tables between any of those. 
 * Initial data was minimal, half-dozen or so data rows is enough for proof of concept. 
 * Executed outside of application to insert necessary "seed" data.
 
 Wrote Python code to:
 * Create a new key
 * Request access to a given room by a given employee
 * Capture the issue of a key to an employee
 * Capture losing a key
 * Report out all the rooms that an employee can enter, given the keys that they already have
 * Delete a key
 * Delete an employee
 * Add a new door that can be opened by an existing hook
 * Update an access request to move it to a new employee
 * Report out all employees who can get into a room
# Description Phase 3
This part of the phase was mostly an exploratory version of phase 2. The point was to do everything we did in phase 2 but using MongoDB instead of SQLAlchemy. This however led to inefficient code as MongoDB has its own strengths that were not fully utilized. The code still works, and I plan to continue to optimize it. 
## Procedure Phase 3
Used UML from phase 1, the focus was on how to implement MongoDB. Had to be creative about how to capture decisions that were made regarding implementation strategy. 
MongoDB has several tools:
* Uniqueness constraints
* References (to simulate relationships)
* MongoDB schemas in collections
Wrote Insert statements to populate:
* Employees, Buildings, rooms, doors, hooks, and other junction collections between any two of those. 
* Executed those outside of application to insert "seed" data
Wrote Python application to update the rest of the collections with menu option to:
* Create a new key
 - Present the user with a list of available hooks
 - Prompt them for which hook they will use to make the key
 - Generate the key number, serial number
* Request access to a given room by a given employee
 - Present the user with a list of the Employees by name and prompt for which one
 - Present the user witha list of the buildings and rooms and prompt for which one
* Capture the issue of a key to an employee
 - This could be part of giving access if you structured your data that way
 - Prompt them for the Access
 - Then code finds the existing key that meets that need, or code creates a new one on a hook that opens at least one of the doors to that room
* Capture losing a key
 - Prompt user for the key request that was lost
 - Capture the date and time of the loss. Default to current date and time
* Report out all the rooms that an employee can enter, given the keys that user already has
 - Prompt for the employee 
 - List the rooms that they have access to
  - Order by building, then room
  - Remove duplicates
* Delete a key
 - Check for any references to that key
  - Either delete the references first
  - Or use try/catch block and let the user know that the key is in use and database cannot delete it
 - Only deletes key if it will not cause an exception to show on screen
* Delete an employee
 - Same cautions as deleting key
* Add a new door that can be opened by an existing hook
 - Prompt them for the hook
 - Prompt them for the Building
 - Propmpt then for the room
 - Provide a menu of available door names and prompt for which door they want
* Update an access request to move it to a new employee
 - Prompt for the old employee
 - Prompt for which access (by room) of theirs that you're to move
 - Prompt for new employee
* Report out all the employees who can get into a room
 - Prompt for the room
 - List the employees by name
# Installation
# Usage
# Contributing
Contributions are welcome. If you find an issue, please open an issue on GitHub repository. If you would like to contribute code, please fork the repository and submit a pull request. 
# License
