#!/bin/env python

from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Length, InputRequired, Email, EqualTo
from project import photos


class RegisterForm(FlaskForm):
    """ Form class to be used when adding a new user """

    name = StringField('NAME:', validators=[InputRequired(
        message='User name cannot be null'), Length(min=4, max=25)])

    email = TextField('EMAIL:', validators=[
                      InputRequired(), Email(message='Email cannot be null')])

    user_image = FileField('User Image', validators=[
                           FileAllowed(photos, 'Images Only!')])

    password = PasswordField('PASSWORD:', validators=[InputRequired(
        message='Pass word cannot be null'), Length(min=4, max=25)])

    confirm_pass = PasswordField('Confirm Password:',
                                 validators=[InputRequired(
                                     message='Password cannot be null'),
                                             Length(min=4, max=25),
                                             EqualTo('password')])


class LoginForm(FlaskForm):
    """ Form class to be used when users log into the application """

    email = TextField('EMAIL:', validators=[
                      InputRequired(), Email(message='Email cannot be null')])
    password = PasswordField('PASSWORD:', validators=[
                             InputRequired(message='Password cannot be null')])
