#!/bin/env python

import os
import sys
from flask import (Flask, Blueprint, render_template, redirect,
                   request, flash, url_for, json)
from flask import session as login_session
from project import photos, lm
from ..db.models import Base, User
from ..db.db_helper import add_newUser, find_user, login_helper
from form_helper import RegisterForm, LoginForm
from flask_login import login_user, login_required, logout_user
from auth_helper import gconnect_helper, g_disconnect_helper
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from flask import make_response, request

user_page = Blueprint('user_page', __name__)

CLIENT_ID = json.loads(
    open('./instance/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"


@user_page.route('/signup', methods=['GET', 'POST'])
def user_signup():
    """ User Signup page """

    # Load the form from the form_helper
    form = RegisterForm()

    # If request method is POST,
    if request.method == 'POST':
        if form.validate_on_submit():

            # Get email from client form input to check
            # if the email is already in the database
            # If exists, send flash message and redirect to the signup page
            email = form.email.data
            if find_user(email):
                flash('User already exists', 'UE')
                return redirect(url_for('user_page.user_signup'))

            # If the user does not exists,
            else:
                name = form.name.data

                # Use default image if no images are selected
                if form.user_image.data is None:
                    filename = 'default_user.png'
                else:
                    filename = photos.save(request.files['user_image'])
                url = photos.url(filename)
                password = form.password.data

                # Execute 'add_newUser' function from db_helper,
                # then register a new user, and redirect to main page
                add_newUser(name, email, password, url)
                return redirect(url_for('catalog_page.get_catalog'))
        else:
            return render_template('signup.html', form=form)
    else:
        return render_template('signup.html', form=form)


@user_page.route('/login', methods=['GET', 'POST'])
def user_login():
    """ User Login page """
    # Generate random state value
    state = state_generator()

    # Store the generated value into the login_session
    login_session['state'] = state

    # Load the form from the form_helper
    form = LoginForm()

    # If request method is POST,
    if request.method == 'POST':
        if form.validate_on_submit():

            # Get the email data from the form and check if
            # the email exists in the database
            # If exists, then send flash message and render the login page with
            # a new randomly generated state value
            email = form.email.data
            if find_user(email) is False:
                flash('User does not exist in the database', 'LE')
                return render_template('login.html', form=form, STATE=state)

            # If the email is not in the database,
            else:
                password = form.password.data

                # Chech if the user input is valid
                user = login_helper(email, password)

                # If the user credentials are valid, then logs in the user,
                # then redirect to the main page
                if user:
                    login_user(user)
                    flash('You are now logged in as %s' % user.username)
                    return redirect(url_for('catalog_page.get_catalog'))

                # If credentials are not valid, then send flash message and
                # render the login page with state value
                else:
                    flash('Username or Password is incorrect', 'LE')
                    return render_template('login.html',
                                           form=form, STATE=state)
        else:
            return render_template('login.html', form=form, STATE=state)
    else:
        return render_template('login.html', form=form, STATE=state)


@user_page.route('/auth/gconnect', methods=['POST'])
def g_signin():
    """ Google Auth Sign in """
    return gconnect_helper()


@user_page.route('/logout')
@login_required
def user_logout():
    """ User Logout page
    This page where users can logout from the application
    Non-authorized users cannot view this page """

    # Logout the user from flask-login session
    logout_user()

    # If the user logged in via google auth,
    # then disconnect google account of the user
    if login_session.get('email') is not None:
        g_disconnect_helper()

    # login_session['email']
    return redirect(url_for('user_page.user_login'))


@user_page.route('/profile/<user_id>')
@login_required
def user_profile(user_id):
    """ User Profile Page
    This page where users can see their
    email, username and their profile picture
    Non-authorized users cannot view this page """

    return render_template('user_profile.html')


# Secret page for testing login session
@user_page.route('/secret')
@login_required
def secret():
    return "secret page"


def state_generator():
    """ Function to generate random token """

    asc = string.ascii_uppercase
    digit = string.digits
    state = ''.join(random.choice(asc + digit) for x in xrange(32))
    return state
