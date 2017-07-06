#!/bin/env python

from sqlalchemy import Column, ForeignKey, Integer, String, Binary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import random
import string
from passlib.hash import bcrypt

Base = declarative_base()


class User(Base):
    """ Class containg User table schema """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    email = Column(String(80))
    picture = Column(String)
    password_hash = Column(Binary)

    def generate_hash(self, password):
        """ Encrypt user password using Bcrypt """

        self.password_hash = bcrypt.hash(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Catalog(Base):
    """ Class containg Catalog table schema """

    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image = Column(String)
    counter = Column(Integer, server_default='0', nullable=False)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'counter': self.counter
        }


class Item(Base):
    """ Class containg Item table schema """

    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog)
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'catalog_id': self.catalog_id,
            'user_id': self.user_id,
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
