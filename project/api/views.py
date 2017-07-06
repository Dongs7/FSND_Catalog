#!/bin/env python

from flask import (Blueprint, render_template, redirect, abort, request,
                   flash, url_for, jsonify)
from ..users.users import login_required, login_session
from ..db.models import Base, Catalog, User, Item
from ..db.db_helper import get_catalogs, get_items_all, get_catalog_items

api_page = Blueprint('api_page', __name__)


@api_page.route('/')
@login_required
def get_api():
    """  Pages in this section require a user_login
    Non-authorized users cannot view or enter this page """

    return render_template('api_main.html')


@api_page.route('/catalog')
@login_required
def get_catalog_api():
    """ The route returns all categories of the catalog in JSON format """

    catalogs = get_catalogs()
    return jsonify(catalogs=[catalog.serialize for catalog in catalogs])


@api_page.route('/items')
@login_required
def get_items_api():
    """ The route returns all items of the catalog in JSON format """
    items = get_items_all()
    return jsonify(items=[item.serialize for item in items])


@api_page.route('/catalog_items')
@login_required
def get_all_api():
    """ """
    catalog_items = get_catalog_items()
    return jsonify(catalog_items=[catalog_item.serialize for catalog_item
                                  in catalog_items])
