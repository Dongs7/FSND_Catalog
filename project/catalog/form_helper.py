#!/bin/env python

from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Length, InputRequired
from project import photos


class AddItem(FlaskForm):
    """ Form class to be used when adding a new item """

    category = SelectField('Choose Category', coerce=int)
    name = StringField(
        'Item Name:',
        validators=[InputRequired(message='This field cannot be null'),
                    Length(min=1, max=30)])

    item_image = FileField(
        'Item Image',
        validators=[FileAllowed(photos, 'Images Only!')])

    desc = TextAreaField(
        'Description: ',
        validators=[InputRequired(message='This field cannot be null')])


class EditItem(FlaskForm):
    """ Form class to be used when modifying an existing item """

    name = StringField(
        'Item Name:',
        validators=[InputRequired(message='This field cannot be null'),
                    Length(min=1, max=30)])

    item_image = FileField(
        'Item Image',
        validators=[FileAllowed(photos, 'Images Only!')])

    description = TextAreaField(
        'Description:',
        validators=[InputRequired(message='This field cannot be null')])
