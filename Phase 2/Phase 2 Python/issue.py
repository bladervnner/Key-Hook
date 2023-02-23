from sqlalchemy import Column, String, Integer, ForeignKey, DATETIME, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from orm_base import Base


class Employees(Base):
    # Table Name
    __tablename__ = 'employees'
    # attributes
    employee_id = Column("employee_id", Integer, nullable=False, primary_key=True)
    name = Column("name", String(35), nullable=False)
    # parent relationships
    requests_list = relationship("Requests", cascade='all,delete', back_populates="employee", viewonly=False)

    # create instance function
    def __init__(self, employee_id: Integer, name: String):
        self.employee_id = employee_id
        self.name = name

        self.requests_list = []


class Requests(Base):
    # Table Name
    __tablename__ = 'requests'
    # attributes
    employee_id = Column("employee_id", Integer, ForeignKey('employees.employee_id'), nullable=False, primary_key=True)
    room_number = Column("room_number", Integer, nullable=False, primary_key=True)
    building_name = Column("building_name", String(40), nullable=False, primary_key=True)
    request_date = Column("request_date", DATETIME, nullable=False, primary_key=True)
    #Foreign Keys
    __table_args__ = (ForeignKeyConstraint(('room_number', 'building_name'),
                                           ('rooms.number', 'rooms.building_name')), {})
    # parent relationships
    issues_list = relationship("Issues", back_populates="request", viewonly=False)
    # child relationships
    room = relationship("Rooms", back_populates="requests_list", viewonly=False)
    employee = relationship("Employees", back_populates="requests_list", viewonly=False)

    # create instance function
    def __init__(self, room, employee, request_date: DATETIME):
        self.employee_id = employee.employee_id
        self.room_number = room.number
        self.building_name = room.building_name
        self.request_date = request_date

        self.issues_list = []

class Issues(Base):
    # Table Name
    __tablename__ = 'issues'
    # attributes
    issue_id = Column("issue_id", Integer, nullable=False, primary_key=True)
    employee_id = Column("employee_id", Integer, nullable=False)
    room_number = Column("room_number", Integer, nullable=False)
    building_name = Column("building_name", String(40), nullable=False)
    request_date = Column("request_date", DATETIME, nullable=False, )
    key_serial_number = Column("key_serial_number", Integer, ForeignKey('keys.key_serial_number'), nullable=False)
    issue_date = Column("issue_date", DATETIME, nullable=False)
    #Foreign Keys
    __table_args__ = (ForeignKeyConstraint(('employee_id', 'room_number', 'building_name', 'request_date'),
                                           ('requests.employee_id', 'requests.room_number', 'requests.building_name',
                                            'requests.request_date')), {})
    # Unique Constraint
    __table_args2__ = (UniqueConstraint('employee_id', 'room_number', 'building_name', 'request_date',
                                       'key_serial_number', 'issue_date'), )
    # parent relationships
    returns_list = relationship("Returns", back_populates="issue", viewonly=False)
    losses_list = relationship("Losses", back_populates="issue", viewonly=False)
    # child relationships
    request = relationship("Requests", back_populates="issues_list", viewonly=False)
    key = relationship("Keys", back_populates="issues_list", viewonly=False)

    # create instance function
    def __init__(self, issue_id: Integer, request, key, issue_date: DATETIME):
        self.issue_id = issue_id
        self.employee_id = request.employee_id
        self.room_number = request.room_number
        self.building_name = request.building_name
        self.request_date = request.request_date
        self.key_serial_number = key.key_serial_number
        self.issue_date = issue_date

        self.returns_list = []
        self.losses_list = []

class Returns(Base):
    # Table Name
    __tablename__ = 'returns'
    # attributes
    issue_id = Column("issue_id", Integer, ForeignKey('issues.issue_id'), nullable=False, primary_key=True)
    return_date = Column("return_date", DATETIME, nullable=False)
    # child relationships
    issue = relationship("Issues", back_populates="returns_list", viewonly=False)

    def __init__(self, issue, return_date: DATETIME):
        self.issue_id = issue.issue_id
        self.return_date = return_date

class Losses(Base):
    # Table Name
    __tablename__ = 'losses'
    # attributes
    issue_id = Column("issue_id", Integer, ForeignKey('issues.issue_id'), nullable=False, primary_key=True)
    loss_date = Column("loss_date", DATETIME, nullable=False)
    # child relationships
    issue = relationship("Issues", back_populates="losses_list", viewonly=False)

    # create instance function
    def __init__(self, issue_id: Integer, loss_date: DATETIME):
        self.issue_id = issue_id
        self.loss_date = loss_date
