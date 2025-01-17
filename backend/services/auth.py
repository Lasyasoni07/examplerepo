from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/sign-up')
def sign_up():
    return "<p>sign up page</p>"

@auth.route('/login')
def login():
    return "<p>login page</p>"

@auth.route('/logout')
def logout():
    return "<p>logout page</p>"

@auth.route('/view-profile')
def view_profile():
    return "<p>view profile page</p>"