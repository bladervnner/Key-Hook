from Utilities import Utilities
'''
1. How to manage _id?
2. How to manage foreign keys?
3. How to manage serial numbers?
'''

buildings_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "A building within the university",
            'required': ["name"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                'name': {
                    'bsonType': "string",
                    "description": "The abbreviation of the name of the building"
                }
            }
        }
    }
}

rooms_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "A room within a building within the university",
            'required': ["building_name", "number"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                '_id': {},
                # FOREIGN KEY
                'building_name': {
                    'bsonType': "string",
                    "description": "The abbreviation of the name of the building"
                },
                'number': {
                    'bsonType': "number",
                    "description": "The room number"
                }
            }
        }
    }
}

doors_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "A door inside a room within a building within the university",
            'required': ["building_name", "room_number", "name"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                '_id': {},
                # FOREIGN KEY
                'building_name': {
                    'bsonType': "string",
                    "description": "The abbreviation of the name of the building"
                },
                # FOREIGN KEY
                'room_number': {
                    'bsonType': "number",
                    "description": "The room number"
                },
                'name': {
                    'bsonType': "string",
                    "description": "The name of the door coming from door_names"
                }
            }
        }
    }
}

door_names_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "A collection of the possible names for a door in the unviersity",
            'required': ["name"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                '_id': {},
                'name': {
                    'bsonType': "string",
                    'description': "a name for the doors",
                    'enum': ["S", "W", "E", "N"]
                }
            }
        }
    }
}

hooks_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "A hook that can open doors in the university",
            'required': ["serial_number"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                '_id': {},
                # Serial Number
                'serial_number': {
                    'bsonType': "number",
                    "description": "A serial number for the hook assigned by the university"
                }
            }
        }
    }
}

keys_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "A copy of the hook",
            'required': ["hook_serial_number", "key_serial_number"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                '_id': {},
                # FOREIGN KEY
                'hook_serial_number': {
                    'bsonType': "number",
                    'description': "A serial number for the hook"
                },
                # Serial Number
                'key_serial_number': {
                    'bsonType': "number",
                    'description': "A serial number for the key"
                }
            }
        }
    }
}

permissions_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "A collection of doors that each hook can open",
            'required': ["hook_serial_number", "building_name", "room_number", "door_name"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                '_id': {},
                # FOREIGN KEY
                'hook_serial_number': {
                    'bsonType': "number",
                    'description': "A serial number for the hook"
                },
                # FOREIGN KEY
                'building_name': {
                    'bsonType': "string",
                    "description": "The abbreviation of the name of the building"
                },
                # FOREIGN KEY
                'room_number': {
                    'bsonType': "number",
                    "description": "The room number"
                },
                # FOREIGN KEY
                'door_name': {
                    'bsonType': "string",
                    "description": "The name of the door"
                }
            }
        }
    }
}

employees_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "An employee that works at the university",
            'required': ["employee_id", "name"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                '_id': {},
                'employee_id': {
                    'bsonType': "number",
                    'description': "An ID assigned by the university to the employee"
                },
                'name': {
                    'bsonType': "string",
                    'description': "The name of the employee"
                }
            }
        }
    }
}

requests_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "A request that is made by an employee for access to a room",
            'required': ["employee_id", "building_name", "room_number", "request_date"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                '_id': {},
                # FOREIGN KEY
                'employee_id': {
                    'bsonType': "number",
                    'description': "The employee ID"
                },
                # FOREIGN KEY
                'building_name': {
                    'bsonType': "string",
                    'description': "The name of the building"
                },
                # FOREIGN KEY
                'room_number': {
                    'bsonType': "number",
                    'description': "The room number"
                },
                'request_date': {
                    # date is a valid attribute?
                    'bsonType': 'date',
                    'description': "The date that the request was made by the employee"
                }
            }
        }
    }
}

issues_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "An issue made by the university to the employee to assign a key for his request",
            'required': ["issue_id", "employee_id", "room_number", "building_name", "request_date",
                         "key_serial_number", "issue_date"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                '_id': {},
                'issue_id': {
                    'bsonType': "number",
                    'description': "An id for the issue"
                },
                # FOREIGN KEY
                'employee_id': {
                    'bsonType': "number",
                    'description': "The employee ID"
                },
                # FOREIGN KEY
                'room_number': {
                    'bsonType': "number",
                    'description': "The room number"
                },
                # FOREIGN KEY
                'building_name': {
                    'bsonType': "string",
                    'description': "The building name"
                },
                # FOREIGN KEY
                'request_date': {
                    # is date a valid type?
                    'bsonType': "date",
                    'description': "The date the request was made"
                },
                # FOREIGN KEY
                'key_serial_number': {
                    'bsonType': "number",
                    'description': "The key serial number"
                },
                'issue_date': {
                    'bsonType': "date",
                    'description': "The date that the issue was made by the university"
                }
            }
        }
    }
}

returns_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "An issue of a key returned by the employee to the university",
            'required': ["issue_id", "return_date"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                '_id': {},
                # FOREIGN KEY
                'issue_id': {
                    'bsonType': "number",
                    'description': "The issue ID"
                },
                'return_date': {
                    # date?
                    'bsonType': "date",
                    'description': "The date that the key was returned"
                }
            }
        }
    }
}

losses_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "An issue of a key lost by the employee",
            'required': ["issue_id", "loss_date"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                '_id': {},
                # FOREIGN KEY
                'issue_id': {
                    'bsonType': "number",
                    'description': "The issue ID"
                },
                'loss_date': {
                    # date?
                    'bsonType': "date",
                    'description': "The date that the key was lost"
                }
            }
        }
    }
}

def validate():
    db = Utilities.startup()
    db.command('collMod', 'buildings', **buildings_validator)
    db.command('collMod', 'rooms', **rooms_validator)
    db.command('collMod', 'doors', **doors_validator)
    db.command('collMod', 'door_names', **door_names_validator)
    db.command('collMod', 'hooks', **hooks_validator)
    db.command('collMod', 'keys', **keys_validator)
    db.command('collMod', 'permissions', **permissions_validator)
    db.command('collMod', 'employees', **employees_validator)
    db.command('collMod', 'requests', **requests_validator)
    db.command('collMod', 'issues', **issues_validator)
    db.command('collMod', 'returns', **returns_validator)
    db.command('collMod', 'losses', **losses_validator)