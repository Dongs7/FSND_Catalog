#!/bin/env python

from flask import (Blueprint, render_template, redirect, abort, request,
                   flash, url_for, jsonify)
from project import photos, lm
from ..users.users import login_required, login_session
import os
from ..db.models import Base, Catalog, User, Item
from form_helper import AddItem, EditItem
from ..db.db_helper import (get_catalogs, get_recent, get_count, get_items,
                            get_badge_count, add_newitem, get_item,
                            modify_item, remove_item, find_duplicate_item)


catalog_page = Blueprint('catalog_page', __name__)


@catalog_page.route('/')
@catalog_page.route('/catalog')
def get_catalog():
    """ # Main Catalog Route
    this page displays the recently added items,
    and all categories of the catalog """

    catalog = get_catalogs()
    recent = get_recent()
    return render_template('index.html',
                           name='catalog_page',
                           counts=catalog,
                           item_lists=recent)


@catalog_page.route('/<catalog_name>/items')
def get_catalog_items(catalog_name):
    """ The page displaying all items of the selected category """
    count = get_count(catalog_name)
    items = get_items(catalog_name)
    return render_template('items.html',
                           c_name=catalog_name,
                           total=count,
                           items=items)


@catalog_page.route('/add_new_item', methods=['GET', 'POST'])
@login_required
def add_item():
    """ # The page where authrorized user can add a new item
    Non-authorized users cannot view this page """

    # Get all categories
    category_list = get_catalogs()

    # Load the form from the form_helper
    form = AddItem()

    # Load all category values and create drop-down list using select tag
    form.category.choices = [(g.id, g.name) for g in category_list]

    # If request method is POST
    if request.method == 'POST':
        if form.validate_on_submit():

            # Get selected category ID
            category_selected = form.category.data

            # Get an item name from the user input
            item_name = form.name.data

            # Check if the item is in the database,
            # send flash message if the item exists,
            # then render the form page again
            if find_duplicate_item(item_name):
                flash('Same item name is already in the database')
                return render_template('add_item.html', form=form)
            # If not in the database,
            else:
                if form.item_image.data is None:
                    filename = 'default_item.png'
                else:
                    filename = photos.save(request.files['item_image'])
                url = photos.url(filename)
                item_description = form.desc.data
                user_id = login_session['user_id']

                # Add the item into the database,
                # send success flash message and redirect to the main page
                add_newitem(category_selected, item_name,
                            url, item_description, user_id)
                flash('New Item successfully Added')
                flash("new", item_name)
                return redirect(url_for('catalog_page.get_catalog'))
        # If form value is not validated, render the same page again
        # WTForm field in the client side will display errors with messages
        else:
            return render_template('add_item.html', form=form)
    # If request method is not POST,
    # render the page with the form
    else:
        return render_template('add_item.html', form=form)


@catalog_page.route('/<catalog_name>/edit/<item_name>',
                    methods=['GET', 'POST'])
@login_required
def edit_item(catalog_name, item_name):
    """ The page where authrorized user can edit the selected item
    Non-authorized users cannot view this page """

    # Get the item to be modified
    item_selected = get_item(item_name)

    # Get all categories of the catalog
    catalog = get_catalogs()

    # Initiate the form with the selected item
    form = EditItem(obj=item_selected)

    # Populate values of the selected item
    form.populate_obj(item_selected)

    # If request method is POST,
    if request.method == 'POST':
        if form.validate_on_submit():

            # Get the value from the select tag
            category_selected = request.form['category_selector']

            # Get the modified name of the item
            edited_name = form.name.data

            # If new photo of the item is added, make new url for the photo
            if form.item_image.data is not None:
                filename = photos.save(request.files['item_image'])
                edited_url = photos.url(filename)

            # Otherwise, use the same url stored in the database
            else:
                edited_url = item_selected.image

            # Get the modified item description
            edited_desc = form.description.data

            # Modify the item by using the helper function, then
            # send success flash message and redirect to the selected page
            modify_item(item_selected, category_selected,
                        edited_name, edited_url, edited_desc)
            flash('Item successfully edited')
            return redirect(url_for('catalog_page.get_catalog_items',
                                    catalog_name=catalog_name))

    # If request method is not POST,
    # render the page with the form
    else:
        return render_template('edit_item.html',
                               c_name=catalog_name,
                               i_name=item_name,
                               category_list=catalog,
                               item=item_selected,
                               form=form)


@catalog_page.route('/<catalog_name>/delete/<item_name>', methods=['POST'])
@login_required
def delete_item(catalog_name, item_name):
    """ The page where authrorized user can delete the selected item
    Non-authorized users cannot view this page """

    # Get the item to be removed
    i_selected = get_item(item_name)

    # If request method is POST,
    if request.method == 'POST':

        # Remove the item by using a helper function,
        # and the return value is True, send flash message and redirect to
        # the selected page
        if remove_item(i_selected):
            flash(i_selected.name +
                  ' is successfully removed from the database')
            return redirect(url_for('catalog_page.get_catalog_items',
                                    catalog_name=catalog_name))

        # If the return is False, print error message
        else:
            return "error occured"
