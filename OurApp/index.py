#APP "/endpoint" here
import sys
sys.path.append(".")
from OurApp import app
from flask import render_template, redirect, url_for


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/user-login", methods=['GET', 'POST'])
def user_login():
    return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def user_register():
    return render_template('register.html')






if __name__ == '__main__':
    app.run(debug=True)