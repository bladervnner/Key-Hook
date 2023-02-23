from sqlalchemy import ForeignKeyConstraint, ForeignKey, Column, String, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from orm_base import Base


class Buildings(Base):
    # Table name
    __tablename__ = 'buildings'
    # attributes
    name = Column("name", String(40), nullable=False, primary_key=True)
    #children
    rooms_list = relationship("Rooms", back_populates="building", viewonly=False)

    #create instance function
    def __init__(self, name: String):
        self.name = name

        self.rooms_list = []



class Rooms(Base):
    from issue import Requests
    # Table name
    __tablename__ = 'rooms'
    # attributes
    building_name = Column("building_name", String(40), ForeignKey('buildings.name'),
                           nullable=False, primary_key=True)
    number = Column("number", Integer, nullable=False, primary_key=True)
    #children
    doors_list = relationship("Doors", back_populates="room", viewonly=False)
    requests_list = relationship("Requests", back_populates="room", viewonly=False)
    #parents
    building = relationship('Buildings', back_populates='rooms_list', viewonly=False)

    # create instance function
    def __init__(self, building, number: Integer):
        self.building_name = building.name
        self.number = number

        self.doors_list = []
        self.requests_list = []
        self.building = building


class DoorNames(Base):
    # Table Name
    __tablename__ = 'door_names'
    # attributes
    name = Column("name", String(15), nullable=False, primary_key=True)
    #children
    doors_list = relationship('Doors', back_populates='doorName', viewonly=False)

    # create instance function
    def __init__(self, name: String):
        self.name = name

        self.doors_list = []


class Doors(Base):
    from access import Permissions
    # Table Name
    __tablename__ = 'doors'
    # attributes
    name = Column("name", String(15), ForeignKey('door_names.name'), nullable=False, primary_key=True)
    room_number = Column("room_number", Integer, nullable=False, primary_key=True)
    building_name = Column("building_name", String(40), nullable=False, primary_key=True)
    #Foreign Keys
    __table_args__ = (ForeignKeyConstraint((room_number, building_name),
                                           (Rooms.number, Rooms.building_name)), {})
    #__table_args__ = (UniqueConstraint('name', 'room_number', 'building_name'),)
    #children
    permissions_list = relationship("Permissions", back_populates="door", viewonly=False)
    #parents
    room = relationship('Rooms', back_populates='doors_list', viewonly=False)
    doorName = relationship('DoorNames', back_populates='doors_list', viewonly=False)

    # create instance function
    def __init__(self, doorName, room):
        self.name = doorName.name
        self.room_number = room.number
        self.building_name = room.building_name

        self.permissions_list = []
        self.room = room
        self.doorName = doorName


