from flask import Flask, render_template
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from flask import request
import utils
import initialize
import pprint

cache = utils.get_redis_connection()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logging.info("Hello!")
initialize.init_sqlite_db()
initialize.load_db_to_redis()
print("OK")
scheduler = BackgroundScheduler()
scheduler.add_job(func=utils.activate_meetings, trigger="interval", seconds=4)
scheduler.start()

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


# Function: a user joins an active meeting instance – if allowed, i.e. his email is in audience
@app.route('/join_meeting/<meeting_signature>/<user_id>', methods=["GET"])
def join_meeting(meeting_signature, user_id):
    try:
        email = resolve_user_email(user_id)
        # at first we check if a meeting is active
        if cache.sismember("active_meetings", f"meeting:{meeting_signature}"):
            # if a meeting has an audience, then the email should be in the audience set
            if (not cache.exists(f"meeting:{meeting_signature}:audience")) or cache.sismember(f"meeting:{meeting_signature}:audience", email):
                cache.sadd(f"meeting:{meeting_signature}:joined", email)
                cache.rpush
            else:
                raise Exception(f"email {email} is not allowed into the meeting!")
        else:
            raise Exception(f"meeting with signature {meeting_signature} not active!")
        return render_template('index.html', posts=[f"Success!"])
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return render_template('index.html', posts=[f"Error:{str(e)}"])


# Function: a user leaves a meeting that has joined
@app.route('/leave_meeting/<meeting_signature>/<user_id>', methods=["GET"])
def leave_meeting(meeting_signature, user_id):
    try:
        email = resolve_user_email(user_id)
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
            return utils.format_results(stmt)
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
                    results.append(cache.hgetall(f"{element}"))
                return utils.format_results(results)
            else:
                return render_template('index.html', posts=[f"Success!\n{stmt}"])
        else:
            return render_template('index.html', posts=[f"There are no active meetings!"])
    except Exception as e:
        logging.error(f"Error:{str(e)}")
        return render_template('index.html', posts=[f"Error:{str(e)}"])

# Function: show active meetings
@app.route('/post_message/<meeting_signature>/<user_id>/<text>', methods={"GET"})
def post_message(meeting_signature, user_id, text):
    try:
        email = resolve_user_email(user_id)
        # at first we check if a meeting is active
        if cache.sismember("active_meetings", meeting_signature):
            # if a meeting has an audience, then the email should be in the audience set
            if cache.sismember(f"meeting:{meeting_signature}:joined", email):
                cache.rpush(f"meeting:{meeting_signature}:messages", text)
                cache.rpush(f"message:{user_id}", text)
                return render_template('index.html', posts=[f"Success!"])
            else:
                raise Exception(f"user with email {email} hasn't joined the meeting is not allowed into the meeting!")
        else:
            raise Exception(f"meeting with signature {meeting_signature} not active!")
        return render_template('index.html', posts=[f"Success!"])
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return render_template('index.html', posts=[f"Error:{str(e)}"])

# Function: 
@app.route('/show_chat/<meeting_signature>', methods={"GET"})
def show_chat(meeting_signature):
    try:
        if cache.sismember("active_meetings", meeting_signature):
            # if a meeting has an audience, then the email should be in the audience set
            result = cache.lrange(f"meeting:{meeting_signature}:messages", 0, -1)
            return render_template('index.html', posts=[f"{result}"])
        else:
            raise Exception(f"meeting with signature {meeting_signature} not active!")
        return render_template('index.html', posts=[f"Success!"])
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return render_template('index.html', posts=[f"Error:{str(e)}"])


@app.route('/get_user_email/<user_id>', methods={"GET"})
def resolve_user_email(user_id):
    result = cache.hmget(f"user:{user_id}", "email")
    if result[0] is None:
        raise Exception("user does not exist")
    return result[0]


def add_event_log(user_id, meeting_signature, type):

    result = cache.hmget(f"user:{user_id}", "email")
    if result[0] is None:
        raise Exception("user does not exist")
    return result[0]
