#!/bin/env python

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from flask import make_response, request, flash
from users import login_user, login_session
from flask_login import login_user
from ..db.models import Base, User
from ..db.db_helper import add_newUser_oauth, find_user, login_helper_auth

CLIENT_ID = json.loads(
    open('./instance/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"


def gconnect_helper():
    ''' Google Oauth Login helper function '''

    print 'PASS'
    if request.args.get('state') != login_session['state']:

        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Get onetime code from the server
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets(
            './instance/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except:
        response = make_response(json.dumps(
            'Failed to upgrade authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v2/tokeninfo?access_token=%s'
           % access_token)

    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error'), 500))
        response.headers['Content-Type'] = 'application/json'

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    stored_credentials = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),   200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    name = login_session['username'] = data['name']
    picture = login_session['picture'] = data['picture']
    email = login_session['email'] = data['email']

    # print 'What is user name?? ', name
    isRegistered = find_user(email)
    if isRegistered is False:
        add_newUser_oauth(name, email, picture)
        user = login_helper_auth(email)
        login_user(user)
    else:
        user = login_helper_auth(email)
        login_user(user)
        print 'user already in database'

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 150px; height: 150px;border-radius: \
     150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Helper function when disconnecting the user from google's oauth


def g_disconnect_helper():
    """ Disconnect the user from google oauth """

    credentials = login_session.get('credentials')
    print 'In gdisconnect access token is %s', credentials
    print 'User name is: '

    if credentials is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    revoke_url = 'https://accounts.google.com/o/oauth2/revoke?token='
    url = revoke_url + login_session['credentials']

    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result

    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
