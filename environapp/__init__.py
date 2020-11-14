import os
import functools

from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from environapp.db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/', methods=('GET', 'POST'))
    def index():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            phoneno = request.form['phoneno']
            print(username)
            print(password)
            print(phoneno)
            db = get_db()
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif not phoneno:
                error = 'Phone number is required.'
            elif db.execute(
                'SELECT id from user WHERE username = ?', (username,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(username)

            if error is None:
                db.execute(
                    'INSERT INTO user (username, password, phoneno) VALUES (?, ?, ?)',
                    (username, generate_password_hash(password), phoneno)
                )
                db.commit()
                return render_template('index.html')

            flash(error)

        return render_template('index.html')

    from . import db
    db.init_app(app)

    return app