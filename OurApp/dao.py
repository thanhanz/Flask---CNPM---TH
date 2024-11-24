#ADD FUNCTION TO QUERY HERE

import hashlib
from OurApp.models import User, Account, Customer
from OurApp import db
import cloudinary.uploader
from flask_login import login_user, logout_user
def add_user(firstName, lastName, phoneNumber, citizenIdentificationCard, gender, dateOfBirth, email, avatar=None):

    customer = Customer(firstName = firstName.strip(),
                lastName=lastName.strip(),
                gender=gender,
                dateOfBirth=dateOfBirth,
                phoneNumber = phoneNumber.strip(),
                citizenIdentificationCard = citizenIdentificationCard.strip(),
                email =email.strip(),
                )

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        customer.avatar=res.get('secure_url')

    db.session.add(customer)
    db.session.commit()

    return customer.id

def add_account(username, password, customerId):
    # Cat chuoi password thanh ma bam
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    account = Account(username=username.strip(),
                      password=password,
                      customer_id=customerId)
    db.session.add(account)
    db.session.commit()

def check_login(username,password):
    password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return Account.query.filter(Account.username.__eq__(username),
                                Account.password.__eq__(password)).first()

def get_customer_by_id(id):
    return Customer.query.get(id)
