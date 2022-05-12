import sqlite3
import datetime
from flask import Flask, render_template
import logging
import initialize
import redis
from apscheduler.schedulers.background import BackgroundScheduler
from flask import request

def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

def get_redis_connection():
    return redis.Redis('localhost', port=6379)

cache = get_redis_connection()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logging.info("Hello!")
initialize.init_sqlite_db()
initialize.load_db_to_redis()
logging.info(cache.hgetall("user:12"))

@app.route('/')
def index():
    return render_template('index.html', posts=["Hello"])

@app.route("/print_all/<table>", methods=["GET"])
def print_table(table):
    with get_db_connection() as conn:
        cursor_obj = conn.cursor()
        query = f"SELECT * FROM {table}"
        result = str(cursor_obj.execute(query).fetchall())
    return result


@app.route('/activate_meeting_instance/<meeting_signature>', methods=["GET"])
def activate_meeting_instance(meeting_signature):
    if cache.exists(f"meeting:{meeting_signature}"):
        cache.sadd("active_meetings", meeting_signature)
    return "Success"

# Function: a user joins an active meeting instance – if allowed, i.e. his email is in audience
@app.route('/join_meeting/<meeting_signature>/<email>', methods=["GET"])
def join_meeting(meeting_signature, email):
    try:
        # at first we check if a meeting is active
        if cache.sismember("active_meetings", meeting_signature):
            # if a meeting has an audience, then the email should be in the audience set
            if (not cache.exists(f"meeting:{meeting_signature}:audience")) or cache.sismember(f"meeting:{meeting_signature}:audience", email):
                cache.sadd(f"meeting:{meeting_signature}:joined", email)
            else:
                raise Exception(f"email {email} is not allowed into the meeting!")
        else:
            raise Exception(f"meeting with signature {meeting_signature} not active!")
        return render_template('index.html', posts=[f"Success!"])
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return render_template('index.html', posts=[f"Error:{str(e)}"])


# Function: a user leaves a meeting that has joined
@app.route('/leave_meeting/<meeting_signature>/<email>', methods=["GET"])
def leave_meeting(meeting_signature, email):
    try:
        try:
            remove_stmt = cache.srem(f"meeting:{meeting_signature}:joined", email)
        except:
            raise(Exception(f"meeting with signature {meeting_signature} is not active!"))
        if remove_stmt:
            return render_template('index.html', posts=[f"Success!"])
        else:
            raise Exception(f"user with email {email} is not found in the meeting!")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return render_template('index.html', posts=[f"Error:{str(e)}"])


# Function: show meeting’s current participants
@app.route('/show_participants/<meeting_signature>', methods=["GET"])
def show_meeting_participants(meeting_signature):
    try:
        stmt = cache.smembers(f"meeting:{meeting_signature}:joined")
        if len(stmt) > 0:
            return render_template('index.html', posts=[f"Success!\n{stmt}"])
        else:
            raise Exception(f"meeting is either inactive or does not exist!")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return render_template('index.html', posts=[f"Error:{str(e)}"])


# Function: show active meetings
@app.route('/show_active_meetings/', methods=["GET"])
@app.route('/show_active_meetings/<detailed>', methods={"GET"})
def show_active_meetings(detailed=None):
    try:
        stmt = cache.smembers("active_meetings")
        results = []
        if len(stmt) > 0:
            if detailed is not None:
                for element in stmt:
                    results.append(cache.hgetall(element))
                return render_template('index.html', posts=[f"Success!\n{results}"])
            else:
                return render_template('index.html', posts=[f"Success!\n{stmt}"])
        else:
            return render_template('index.html', posts=[f"There are no active meetings!"])
    except Exception as e:
        logging.error(f"Error:{str(e)}")
        return render_template('index.html', posts=[f"Error:{str(e)}"])
