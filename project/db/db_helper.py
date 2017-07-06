#!/bin/env python

from sqlalchemy import create_engine, exists, func
from sqlalchemy.orm import relationship, sessionmaker
from models import Base, User, Catalog, Item
from project import lm, photos
engine = create_engine('sqlite:///project/db/catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# User DB Helper Functions


@lm.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id=user_id).first()


def get_userInfo(user_id):
    """ Returns the user whose ID matches with passed parameter """

    q = session.query(User).filter_by(id=user_id).one()
    return q


def add_newUser(name, email, password, url):
    """ Register a new user into the database """

    newUser = User(username=name, email=email, picture=url)
    newUser.generate_hash(password)
    session.add(newUser)
    session.commit()


def add_newUser_oauth(name, email, url):
    """ Register a new user who logged in via oauth into the database """

    newUser = User(username=name, email=email, picture=url)
    session.add(newUser)
    session.commit()


def find_user(value):
    """ Check if the user is in the database
    Return True if exists, False otherwise """

    find = session.query(exists().where(User.email == value)).scalar()
    return find


def login_helper(email, password):
    """ Find the user by email
    If found, verify password
    Return the user if found, False otherwise """

    user = session.query(User).filter_by(email=email).one()
    if user:
        if user.verify_password(password):
            return user
        else:
            return False


def login_helper_auth(email):
    """ Users trying to log in via oauth do not have password
    Thus, check if the user email is in the data """

    return session.query(User).filter_by(email=email).one()


def get_catalogs():
    """ Get all categories of the catalog """

    catalog = session.query(Catalog).all()
    return catalog


def get_items_all():
    """ Get all items in the database. Sort them by their catalog id """

    items = session.query(Item).order_by(Item.catalog_id).all()
    return items


def get_catalog_items():
    """ Basically same as above, need to check again """

    q = session.query(Item).join(Catalog).order_by(Catalog.id).all()
    return q


def get_badge_count():
    """ Return a total number of items of each categories """

    b_count = session.query(func.count(Item.catalog_id), Catalog.name,
                            Catalog.image).filter_by(
        catalog_id=Catalog.id).group_by(Catalog.name).all()
    return b_count


def get_recent():
    """ Return recently added items. Only 10 items will be shown """

    recent_items = recent_items = session.query(Item).join(
        Catalog).order_by('item.id desc').limit(10)
    return recent_items


def get_items(cata_name):
    """ Return all items of the selected category """

    items = session.query(Item).join(Catalog).filter(
        Catalog.name == cata_name).all()
    return items

def get_item_category(category_id):
    """ Return a matching category """

    cate = session.query(Catalog).filter_by(id = category_id).one()
    return cate

def find_duplicate_item(item_name):
    """ Check if the item is in the database
    Return True if exists, False otherwise """

    find = session.query(exists().where(Item.name == item_name)).scalar()
    return find


def get_count(cata_name):
    """ Return a total number of items of the selected category """

    count = session.query(Item).join(Catalog).filter(
        Catalog.name == cata_name).count()
    return count


def add_newitem(cate, name, url, desc, user_id):
    """ Helper function when adding a new item in the database """

    newItem = Item(name=name, image=url, description=desc,
                   user_id=user_id, catalog_id=cate)
    targetCategory = get_item_category(cate)
    targetCategory.counter = targetCategory.counter + 1
    session.add(newItem)
    session.commit()
    session.add(targetCategory)
    session.commit()


def get_item(item_name):
    """ Return a specific item """

    item = session.query(Item).filter_by(name=item_name).one()
    return item


def modify_item(item, cate, name, url, desc):
    """ Helper function when modifying the item """

    editItem = item
    editItem.catalog_id = cate
    editItem.name = name
    editItem.description = desc
    editItem.image = url
    session.add(editItem)
    session.commit()


def remove_item(item):
    """ Helper function when deleting the item  """

    try:
        targetCategory = get_item_category(item.catalog_id)
        targetCategory.counter = targetCategory.counter - 1
        session.delete(item)
        session.add(targetCategory)
        session.commit()
        return True
    except:
        return False
