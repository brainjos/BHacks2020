import os
import functools

from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from environapp.db import get_db
from twilio.rest import Client

account_sid = "ACa2265e40cf5d0e64787899eff0170023"
auth_token = "b217f03dc0715d6dab5ef35b7200db99"
client = Client(account_sid, auth_token)

def welcome_message(username, phoneno):
    message = client.messages \
    .create(
         body='Welcome to the Environmental Check-In App, %s!' % username,
         from_='+12543263257',
         to= phoneno
     )

from twilio.twiml.messaging_response import MessagingResponse

from models import *


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

    # load questions
    LOADED_QUESTIONS = None
    with open('./questions.json') as f:
        print(f)
        LOADED_QUESTIONS = load_questions(f)

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
            elif not phoneno or not phoneno.isdigit():
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
                welcome_message(username, phoneno)
                return render_template('index.html')

            flash(error)

        return render_template('index.html')


    # respond to user's messages
    @app.route('/sms', methods=['GET, POST'])
    def reply():
        response = MessagingResponse()

        if 'question_id' in session:
            response.redirect(url_for('answer', question_id=session['question_id']))
        else:
            start_questions()


        return str(response)

    # first question
    def start_questions(response):
        response.redirect(url=url_for('question', question_id=0), method='GET')

    # ask question
    # question id = index
    @app.route('/question/<question_id>')
    def question(question_id):
        try:
            question = LOADED_QUESTIONS[question_id]
        except IndexError:
            print(f"Question of id {question_id} does not exist.")

        session['question_id'] = question_id

        return sms_response(question)

    def sms_response(question):
        response = MessagingResponse()
        response.message(question.prompt)

        return str(response)


    # handle user response
    @app.route('/answer/<question_id>', methods=['POST'])
    def answer(question_id):
        question = LOADED_QUESTIONS[question_id]
        print(question_id, " answered")
        # database = None # placeholder

        # database.save("something") #placeholder

        c = session.get('question_id', 0)
        c += 1
        session['question_id'] = c

        # does this question exist?
        if(c < len(LOADED_QUESTIONS)):
            return go_to_question(c)

        else:
            return finished_message()


    def go_to_question(question_id):
        response = MessagingResponse()
        response.redirect(url=url_for('question', question_id=question_id), method='GET')

        return str(response)

    
    # end result
    def finished_message():
        print(f"{request.values['MessageSid']} is done")
        return "done"



    from . import db
    db.init_app(app)

    return app