# Key-Hook

Key-Hook is a Python based key and access management system developed using PostgreSQL and MongoDB.

The project focuses on managing physical keys, employees, buildings, rooms, and access permissions. It allows users to create and issue keys, track lost keys, manage employee access requests, and generate reports showing which employees can access specific rooms.

The project was developed in three phases:

- Phase 1: Designed the database using business rules, UML models, and an entity-relationship diagram (ERD).
- Phase 2: Implemented a relational database using PostgreSQL and SQLAlchemy, with a Python console application for managing records.
- Phase 3: Reimplemented the system using MongoDB and PyMongo to explore a document-oriented approach to the same problem.

## Procedure Phase 1
1. UML model all business rules from business rules (seperate file)
2. For each of the business rules that cannot be implemented by the way the database is structured, write out pseudo code how those business rules will be implemented using Python code.
3. Once UML model (seperate file) has been completed, the next step is to build an ERD diagram. We will not implement tables for the ERD diagram. Instead, SQLAlchemy will build the tables for us.

## Description Phase 2
Using SQLAlchemy to access a back-end database in PostgreSQL that is structured according to the phase 1 design
The goal of this phase is to demonstrate the use of SQLAlchemy in a console application. Application uses a hybrid approach to populate some of the tables. Insert, Update, and Delete data are achieved using SQLAlchemy. The code design handles any data input from the user. 
### Procedure Phase 2
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
## Description Phase 3
This part of the phase was mostly an exploratory version of phase 2. The point was to do everything we did in phase 2 but using MongoDB instead of SQLAlchemy. This however led to inefficient code as MongoDB has its own strengths that were not fully utilized. The code still works, and I plan to continue to optimize it. 
### Procedure Phase 3
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

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/bladervnner/Key-Hook.git
cd Key-Hook
```

### 2. Install dependencies

Make sure Python 3 and pip are installed.

```bash
python -m pip install -r requirements.txt
```

### 3. Configure database connections

The project includes two database implementations:

- **Phase 2:** PostgreSQL with SQLAlchemy.
- **Phase 3:** MongoDB with PyMongo.

Copy `.env.example` to a new file named `.env` in the project root.

Update the connection strings with your own database credentials:

```dotenv
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/keyhook
MONGODB_URI=mongodb+srv://username:password@cluster.example.mongodb.net/
```

The `.env` file is excluded from Git to prevent credentials from being committed.

### 4. Database setup

For PostgreSQL, install PostgreSQL and create a database:

```sql
CREATE DATABASE keyhook;
```

For MongoDB, configure a MongoDB Atlas deployment and database user.

Database schemas and initial records must be configured according to the corresponding phase's implementation before running the application.

## Usage

Key-Hook has two Python console applications, one using PostgreSQL and the other using MongoDB.

### Phase 2: PostgreSQL

From the repository root:

```bash
cd "Phase 2/Phase 2 Python"
python main.py
```

### Phase 3: MongoDB

From the repository root:

```bash
cd "Phase 3"
python main.py
```

Both apps provide menu options for managing keys, employees, room access requests and generating access reports.

**Note:** Both implementations require their respective databases to be configured and populated with the necessary initial records before use.
## Contributing
Contributions are welcome. If you find an issue, please open an issue on GitHub repository. If you would like to contribute code, please fork the repository and submit a pull request. 
