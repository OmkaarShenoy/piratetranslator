#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os

import requests
import json

# Maximum length of string after modifications.
MAX = 1000;


# Replaces spaces with %20 in-place and returns
# new length of modified string. It returns -1
# if modified string cannot be stored in str[]
def replaceSpaces(string):
    # Remove remove leading and trailing spaces
    string = string.strip()

    i = len(string)

    # count spaces and find current length
    space_count = string.count(' ')

    # Find new length.
    new_length = i + space_count * 2

    # New length must be smaller than length
    # of string provided.
    if new_length > MAX:
        return -1

    # Start filling character from end
    index = new_length - 1

    string = list(string)

    # Fill string array
    for f in range(i - 2, new_length - 2):
        string.append('0')

    # Fill rest of the string from end
    for j in range(i - 1, 0, -1):

        # inserts %20 in place of space
        if string[j] == ' ':
            string[index] = '0'
            string[index - 1] = '2'
            string[index - 2] = '%'
            index = index - 3
        else:
            string[index] = string[j]
            index -= 1

    return ''.join(string)


# This code is contributed by Vinayak




#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    user_ip = request.form['user_input']
    text = replaceSpaces(user_ip)
    response = requests.get("https://pirate.monkeyness.com/api/translate?english=" + text)
    data = response.text
    #parse_json = json.loads(data)
    #translated = parse_json['contents']['translated']
    return render_template('pages/result.html', result=data)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
