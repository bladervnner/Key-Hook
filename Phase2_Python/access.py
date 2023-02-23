from sqlalchemy import ForeignKey, Column, String, Integer, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from orm_base import Base

class Hooks(Base):
    # Table Name
    __tablename__ = 'hooks'
    # attributes
    serial_number = Column("serial_number", Integer, primary_key=True)
    # parent relationships
    permissions_list = relationship("Permissions", back_populates="hook", viewonly=False)
    keys_list = relationship("Keys", back_populates="hook", viewonly=False)

    # create instance function
    def __init__(self, serial_number: Integer):
        self.serial_number = serial_number

        self.doors_list = []
        self.keys_list = []

    def __str__(self):
        return "serial_number: {number}".format(number = self.serial_number)



class Keys(Base):
    # Table Name
    __tablename__ = 'keys'
    # attributes
    key_serial_number = Column("key_serial_number", Integer, nullable=False, primary_key=True)
    hook_serial_number = Column("hook_serial_number", Integer, ForeignKey('hooks.serial_number'), nullable=False)
    # parent relationships
    issues_list = relationship("Issues", back_populates="key", viewonly=False)
    # child relationships
    hook = relationship("Hooks", back_populates="keys_list", viewonly=False)

    # create instance function
    def __init__(self, hook, key_serial_number: Integer):
        self.key_serial_number = key_serial_number
        self.hook_serial_number = hook.serial_number

        self.issues_list = []

class Permissions(Base):

    # Table Name
    __tablename__ = 'permissions'
    # attributes
    hook_serial_number = Column("hook_serial_number", Integer, ForeignKey('hooks.serial_number'), nullable=False, primary_key=True)
    room_number = Column("room_number", Integer, nullable=False, primary_key=True)
    building_name = Column("building_name", String(40), nullable=False, primary_key=True)
    door_name = Column("door_name", String(15), nullable=False, primary_key=True)
    # child relationships
    door = relationship('Doors', back_populates="permissions_list", viewonly=False)
    hook = relationship('Hooks', back_populates="permissions_list", viewonly=False)
    #Foreign Keys
    #If I try this approach it gives the error "sqlalchemy.exc.ArgumentError: ForeignKeyConstraint on Hook_Project.permissions(hook_serial_number, room_number, building_name, door_name) refers to multiple remote tables: doors and hooks"
    #__table_args__ = (ForeignKeyConstraint(['hook_serial_number', 'room_number', 'building_name', 'door_name'],
                                           #['hooks.serial_number', 'doors.room_number', 'doors.building_name', 'doors.name']), {})
    #If I try this approach, it gives the error "NameError: name 'Hooks' is not defined"

    __table_args__ = (ForeignKeyConstraint(['room_number', 'building_name', 'door_name'],
                                        ['doors.room_number', 'doors.building_name', 'doors.name']), {})

    #__table_args__ = (UniqueConstraint('hook_serial_number', 'room_number', 'building_name', 'door_name'),)
    '''
    __tablename__ = 'permissions'
    permissions = Table("permissions",
                        Base.metadata,
                        Column("hook_serial_number", Integer, ForeignKey('hooks.serial_number'), nullable=False, primary_key=True),
                        Column("room_number", Integer, ForeignKey('doors.room_number'), nullable=False, primary_key=True),
                        Column("building_name", String(40), ForeignKey('doors.building_name'), nullable=False, primary_key=True),
                        Column("door_name", String(15), ForeignKey('doors.name'),nullable=False, primary_key=True))
    '''

    # create instance function
    def __init__(self, hook, door):
        self.hook_serial_number = hook.serial_number
        self.room_number = door.room_number
        self.building_name = door.building_name
        self.door_name = door.name

        self.door = door
        self.hook = hook