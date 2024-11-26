import sys
sys.path.append("D:/PrjQLKS/HotelManageApp")

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Double, Enum as EnumRole, \
    UniqueConstraint, Table
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from enum import Enum
from OurApp import app, db
from flask_login import UserMixin
from flask_migrate import Migrate

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)

class UserRole(Enum):
    ADMIN = 1
    EMPLOYEE = 2
    CUSTOMER = 3

#class Role


class User(BaseModel, UserMixin):
    __abstract__ = True
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    email = Column(String(50))
    phoneNumber = Column(String(20), nullable=False)
    gender = Column(String(10), nullable=False)
    avatar = Column(String(100))
    citizenIdentificationCard = Column(String(20), nullable=False)
    dateOfBirth = Column(DateTime)

    @property
    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.id)

class Customer(User):
    # (One - to - one) relationship -> use back_populates

    #lazy=True chi? xuat hien khi duoc. goi: customer.account
    account = relationship('Account', back_populates='customer', uselist=False, lazy=True)
    passport = relationship('Passport', back_populates='customer', uselist=False, lazy=True)

    #(One-to-Many)
    booking=relationship('Booking', backref='customer')
    renting_detail=relationship('RentingDetail', backref='customer', lazy=True)


    def __str__(self):
        return self.firstName + self.lastName



class Account(BaseModel):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    #ENUM
    userRole = Column(EnumRole(UserRole), default=UserRole.CUSTOMER)

    #rela
    customer=relationship('Customer', back_populates='account', lazy=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    employee=relationship('Employee', back_populates='account', lazy=True)
    employee_id=Column(Integer, ForeignKey('employee.id'))

    def __str__(self):
        return self.username


class Country(BaseModel):
    countryName = Column(String(50), nullable=False)

    passport=relationship('Passport', backref='country', lazy=True)
    address=relationship('Address', backref='country', lazy=True)

    def __str__(self):
        return self.countryName


class Address(BaseModel):
    address = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)

    country_id=Column(Integer, ForeignKey(Country.id), nullable=False)

    def __str__(self):
        return self.address


class Passport(BaseModel):
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    ppNumber = Column(String(25), nullable=False)

    #
    customer = relationship('Customer', back_populates='passport', lazy=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    country_id=Column(Integer, ForeignKey(Country.id), nullable=False)

    def __str__(self):
        return self.ppNumber


class Employee(User):

    workingDate = Column(DateTime, default=datetime.now())
    salary = Column(Double, nullable=False)
    #
    account = relationship('Account', back_populates='employee', uselist=False, lazy=True)
    invoices=relationship('Invoice', backref='employee', lazy=True)
    booking=relationship('Booking', backref='booking', lazy=True)
    renting=relationship('Renting', backref='renting', lazy=True)

    def __str__(self):
        return self.firstName + self.lastName


class BookingMethod(BaseModel):
    name=Column(String(20), nullable=False)
    description=Column(String(100))
    #Rela
    booking=relationship('Booking', backref='bookingMethod', lazy=True)

    def __str__(self):
        return self.name


class BookingStatus(BaseModel):
    name = Column(String(20), nullable=False)
    description = Column(String(100))
    #Rela
    booking = relationship('Booking', backref='bookingStatus', lazy=True)

    def __str__(self):
        return self.name


#TABLE(N-N)
class BookingDetail(BaseModel):
    numberRooms = Column(Integer, default=1)
    note = Column(String(50))
    #ForeignKey
    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    roomType_id = Column(Integer, ForeignKey('room_type.id'), nullable=False)

    #Unique config
    __table_args__=(UniqueConstraint('booking_id', 'roomType_id',name='booking_roomType_unique'),)


class Booking(BaseModel): #Phieu dat
    checkInDate = Column(DateTime, default = datetime.now())
    checkOutDate = Column(DateTime, default=datetime.now())
    note = Column(String(100))
    numberRooms = Column(Integer, default=1)
    numberStayGuests = Column(Integer, default=1)
    deposit = Column(Double)

    #ForeignKey
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    employee_id=Column(Integer, ForeignKey(Employee.id), nullable=False)
    bookingMethod_id=Column(Integer, ForeignKey(BookingMethod.id), nullable=False)
    bookingStatus_id=Column(Integer, ForeignKey(BookingStatus.id), nullable=False)

    #Relation (n-n)
    roomTypes=relationship('RoomType', secondary='booking_detail', back_populates='bookings' )

    def __str__(self):
        return self.deposit


class RoomType(BaseModel):
    name = Column(String(20), nullable=False)
    description = Column(String(100))
    maxNumberOfCustomer = Column(Integer, default=1)
    price = Column(Double, nullable=False)
    thumbnail = Column(String(100))
    #Rela
    bookings = relationship('Booking', secondary='booking_detail', back_populates='roomTypes')
    rooms=relationship('Room', backref='roomType', lazy=True)

    def __str__(self):
        return self.name


#TABLE (n-n)
class RentingDetail(BaseModel):
    #ForeignKey
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    renting_id = Column(Integer, ForeignKey('renting.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

    #Unique cfg
    __table_args__=(UniqueConstraint('room_id', 'renting_id',name='room_renting_unique'),)

class PaymentMethod(BaseModel):
    name = Column(String(50))

    invoices=relationship('Invoice', backref='payment_method', lazy=True)

    def __str__(self):
        return self.name


class ServiceType(BaseModel):
    name = Column(String(50), nullable=False)

    service=relationship('Service', backref='serviceType', lazy=True)

    def __str__(self):
        return self.name


class Service(BaseModel):
    name = Column(String(50), nullable=False)
    price = Column(Double)
    unit = Column(Double)

    invoiceDetail=relationship('InvoiceDetail', backref='service', lazy=True)
    serviceType_id=Column(Integer, ForeignKey(ServiceType.id), nullable=False)

    def __str__(self):
        return self.name


class Invoice(BaseModel):
    totalMoney = Column(Double, nullable=False)
    deposit = Column(Double)
    surcharge = Column(Double)
    note = Column(String(100))
    discount = Column(Double)

    #1-n (Aggregation)
    paymentMethod_id=Column(Integer, ForeignKey(PaymentMethod.id), nullable=False)
    employee_id=Column(Integer,ForeignKey(Employee.id), nullable=False)

    #1-1
    renting=relationship('Renting',back_populates='invoice', uselist=False, lazy=False)
    #Composition -> cascade
    details=relationship('InvoiceDetail', cascade='all, delete-orphan'
                                                      , back_populates='invoice')

    def __str__(self):
        return self.totalMoney


class InvoiceDetail(BaseModel):
    number = Column(Integer)
    totalMoney = Column(Double)

    #ForeignKey
    invoice_id=Column(Integer, ForeignKey(Invoice.id), nullable=False)
    invoice=relationship('Invoice', back_populates='details', lazy=True)

    service_id=Column(Integer, ForeignKey(Service.id), nullable=False)



class Renting(BaseModel): #Phiếu thuê
    checkInDate = Column(DateTime, default=datetime.now())
    checkOutDate = Column(DateTime, default=datetime.now())
    note = Column(String(100))

    #ForeignKey
    employee_id=Column(Integer,ForeignKey(Employee.id), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    invoice_id = Column(Integer, ForeignKey(Invoice.id), nullable=False)

    #1-1
    invoice = relationship('Invoice', back_populates='renting', lazy=True)
    #n-n
    rooms=relationship('Room', back_populates='renting', secondary='renting_detail')

class RoomStatus(BaseModel):
    name = Column(String(50))
    description = Column(String(100))
    #Rela
    rooms=relationship('Room', backref='roomStatus', lazy=True)

    def __str__(self):
        return self.name


class Room(BaseModel):
    name = Column(String(20), nullable=False)
    note = Column(String(50))
    floor = Column(Integer)
    thumbnail = Column(String(100), nullable=False)

    # Rela
    renting = relationship('Renting', back_populates='rooms', secondary='renting_detail')
    images= relationship('ImgRoom', back_populates='room', cascade="all, delete-orphan") #(1-N)
    # ForeignKey
    roomStatus_id = Column(Integer, ForeignKey(RoomStatus.id), default=3)
    roomType_id = Column(Integer, ForeignKey(RoomType.id), nullable=False)


    def __str__(self):
        return self.name

class ImgRoom(BaseModel):
    image_url = Column(String(200), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'))

    room = relationship('Room', back_populates='images')

    def __str__(self):
        return self.image_url

if __name__ == '__main__':
    with app.app_context():
         db.create_all()



