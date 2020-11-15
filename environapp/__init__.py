import os
import functools

from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
from werkzeug.security import check_password_hash, generate_password_hash
from environapp.db import get_db
from twilio.rest import Client

# not in git repo, make your own with:
# ACCOUNT_SID, AUTH_TOKEN
# Twilio number with area code (ex: +1XXXXXXXXXX)
# Flask secret key

from environapp.settings import *

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def welcome_message(username, phoneno):
    number_with_area_code = '+1' + phoneno
    message = client.messages \
    .create(
         body='Welcome to the Environmental Check-In App, %s!' % username,
        #  from_='+12543263257',
        from_=twphonenum,
         to= number_with_area_code
     )

from twilio.twiml.messaging_response import MessagingResponse

from environapp.models import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # load questions
    LOADED_QUESTIONS = None
    with app.open_resource('questions.json') as f:
        LOADED_QUESTIONS = load_questions(f.read().decode('utf-8'))

    # load favicon, don't know if need this
    @app.route('/favicon.ico') 
    def favicon():
        return send_from_directory('static', 'favicon.ico')

    # a simple page that says hello
    @app.route('/', methods=('GET', 'POST'))
    def index():
        if request.method == 'POST':

            if 'question_id' in session and session['question_id']:
                del session['question_id']

            username = request.form['username']
            password = request.form['password']
            phoneno = request.form['phoneno']

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
    # NOTE: In order for this to work: https://twilio-cms-prod.s3.amazonaws.com/images/automated-survey-webhook.width-800.png
    # set the webhook under Messaging to the url of your flask app
    @app.route('/sms', methods=['GET', 'POST'])
    def reply():
        IS_RECEIVING = True #placeholder. in future will be timed/scheduled
        if not IS_RECEIVING:
            return

        print(f"receive from {request.values.get('From')}")
        response = MessagingResponse()

        # if we've already asked another question, then go to the next one
        if 'question_id' in session:
            response.redirect(url_for('answer', question_id=session['question_id']))
        # otherwise, start asking with the first question
        else:
            start_questions(response)


        return str(response)

    # first question
    def start_questions(response):
        session['question_id'] = 0
        response.redirect(url=url_for('question', question_id=0), method='GET')

    # ask question
    # question id = index
    @app.route('/question/<question_id>')
    def question(question_id):
        # id is integer (index)
        id = int(question_id)

        print("asking ", id)

        try:
            question = LOADED_QUESTIONS[id]
        except IndexError:
            print(f"Question of id {id} does not exist.")

        session['question_id'] = id

        return sms_response(question)

    def sms_response(question):
        response = MessagingResponse()
        response.message(question.prompt)

        return str(response)


    # handle user response
    @app.route('/answer/<question_id>', methods=['POST'])
    def answer(question_id):
        id = int(question_id)
        print("you are on ", id)
        if id >= len(LOADED_QUESTIONS):
            return finished_message()

        question = LOADED_QUESTIONS[id]

        # if the answer is not in the correct format then ask again
        if not handle_answer(id):
            return go_to_question(id, True)

        # get the current question for this session and add one (go to next question)
        c = session.get('question_id', 0)
        c += 1
        session['question_id'] = c

        # does this question exist?
        if(c < len(LOADED_QUESTIONS)):
            return go_to_question(c)

        else:
            return finished_message()


    # reask: if we have already asked this question but the user gave an invalid answer
    def go_to_question(question_id, reask=False):
        response = MessagingResponse()
        response.message("Please send a valid input. ")
        response.redirect(url=url_for('question', question_id=question_id), method='GET')

        return str(response)


    def handle_answer(id):
        question = LOADED_QUESTIONS[id]
        ans = request.values['Body']
        print(id, " answered with ", ans)

        # attempt to format as int (i) or string (s)
        if question.response == 'i':
            try:
                ansF = int(ans)
            except ValueError:
                return False
        
        elif question.response == 's':
            ansF = ans

        print("Got response ", ansF)

        # TODO: Store ansF in database

        # db = get_db()
        # db.execute(
        #     # 'INSERT INTO user (username, password, phoneno) VALUES (?, ?, ?)',
        #     # (username, generate_password_hash(password), phoneno)
        # )
        # db.commit()

        return ansF

    
    # end result
    def finished_message():
        # if 'question_id' in session:
        #     del session['question_id'] 
        print(f"{request.values['MessageSid']} is done")
        return "done"



    from . import db
    db.init_app(app)

    return app