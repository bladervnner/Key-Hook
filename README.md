# Key-Hook
Project to gain experience using a programming language(Python) to interface between the user and the database used to serialize the data the user is inputting.

# Description

The Key Hook Management System is a three-part term project that provices a programming interface for the user to interact with the database used to serialize data related to the key and lock system at a public university. This project is designed to help employees (staff or faculty) manage their access to rooms withi the university's buildings using a unique key hook system. 

The project is designed to handle the followowing aspects of the key and lock system:

* Employee requests for access to a specific room
* Employeee identification using their ID number
* Unique identification of each room within a building using an integer room number
* Tracking of employee requests and when they were made
* Doors within a room identified by their unique names
* Management of the master key (hook) system
* Tracking of key issuance to employees based on their request and date/time of issuance
* Tracking of key returns and availability for re-issuance
* Management of lost keys and the associated $25 charge
* Ensuring that a key is never issued unless it has been requested
* Preventing the issuance of two identical keys to the same employee based on the same hook, including the handling of multiple access requests for rooms that share a hook

The project is built using Python and is designed to provide a user-friendly interface for managing the keyh hook system. The aim of the project is to provide university staff and faculty with an efficient and effective tool fo rmanaging access to rooms within university buildings. 

# Procedure Phase 1
1. UML model all business rules from business rules (seperate file)
2. For each of the business rules that cannot be implemented by the way the database is structured, write out pseudo code how those business rules will be inplemented using Python code.
3. Once UML model (seperate file) has been completed, the next step is to build an ERD diagram. We will not implement tables for the ERD diagram however. Instead, SQLAlchemy will build the tables for us.
