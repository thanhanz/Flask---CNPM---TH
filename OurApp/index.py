#APP "/endpoint" here
import sys
from OurApp.dao import check_login, get_customer_by_id

sys.path.append(".")
from OurApp import app, dao, login
from flask import render_template, redirect, url_for, request
import logging
from flask_login import login_user, logout_user, current_user




@app.route("/")
def home():
    rts = dao.load_list_roomtypes()
    rooms = dao.load_list_room()

    return render_template('index.html', roomtypes=rts, rooms=rooms)

@app.route("/login", methods=['GET', 'POST'])
def user_login():

    err_msg=None

    if request.method.__eq__('POST'):
        username=request.form.get('username')
        password = request.form.get('password')

        account = dao.check_login(username=username,password=password)

        if account:
            u = dao.get_customer_by_id(account.customer_id)
            login_user(u)
            return redirect("/")
        else:
            err_msg="Your account isn't exist or wrong passworrd!, do again!!"

    return render_template('login.html', err_msg=err_msg)

@login.user_loader
def user_load(user_id):
    return dao.get_customer_by_id(user_id)

@app.route("/logout")
def user_logout():
    logout_user()
    return redirect("/")



@app.route("/register", methods=['GET', 'POST'])
def register():

    err_msg=None

    if request.method.__eq__('POST'):
        confirm= request.form.get('confirm')
        username=request.form.get('username')
        password=request.form.get('password')

        if password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']
            del data['username']
            del data['password']

            avatar = request.files.get('avatar')
            customerId=dao.add_user(avatar=avatar, **data)
            dao.add_account(username=username,password=password,customerId=customerId)

            return redirect("/login")
        else:
            err_msg='Passwords do not match'
    return render_template('register.html', err_msg=err_msg)



if __name__ == '__main__':
    app.run(debug=True)