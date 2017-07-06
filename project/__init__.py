#!/bin/env python

from flask import Flask, url_for, redirect, render_template, Blueprint
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads

# Initialize app and apply app settings from flask config file
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

# Initialize Flask_Login and register app to it
lm = LoginManager()
lm.init_app(app)


# Configure settings for Flask_uploads
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Initialize flask_bootstrap and register app to it
Bootstrap(app)

# Register Blueprints
from catalog.catalog import catalog_page
from users.users import user_page
from api.views import api_page

app.register_blueprint(catalog_page)
app.register_blueprint(user_page, url_prefix='/users')
app.register_blueprint(api_page, url_prefix='/api')
