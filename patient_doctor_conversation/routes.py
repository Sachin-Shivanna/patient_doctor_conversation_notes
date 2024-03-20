from flask import Blueprint, render_template, flash, redirect, url_for
from patient_doctor_conversation.forms import LoginForm
from patient_doctor_conversation.route_handlers.form_submission_handler import handle_form_submission


main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)


"""
Render the index.html template with the title 'Home'.

This function is a route decorator that maps the URL '/' and '/index' to this function.
It returns the rendered template 'index.html' with the title 'Home'.

Returns:
    The rendered template 'index.html' with the title 'Home'.
"""
@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Home')

""" 
A function to handle form submission when a POST request is made to the '/submit' route.
"""
@main.route('/submit', methods=[ 'POST'])
def submit():
    return handle_form_submission()


"""
    Handles the login functionality for the '/login' route.

    Parameters:
    - None

    Returns:
    - If the login form is successfully submitted, the user is redirected to the 'main.index' route.
    - If the login form is not submitted or fails validation, the login page is rendered with the provided form.

    Note:
    - This function is decorated with the '@auth.route' decorator to specify the route '/login' and the supported HTTP methods ('GET', 'POST').
    - The 'form' variable is an instance of the 'LoginForm' class, which is used to handle the login form data.
    - The 'flash' function is used to display a flash message indicating the username of the user attempting to log in.
    - The 'redirect' function is used to redirect the user to the 'main.index' route after successful login.
    - The 'render_template' function is used to render the 'login.html' template with the specified title and form.
"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.username.data))
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)
