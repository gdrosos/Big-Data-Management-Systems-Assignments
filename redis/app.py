from datetime import datetime
import traceback
from flask import Flask, render_template
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from flask import request
import utils
import initialize
import pprint

cache = utils.get_redis_connection()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logging.info("Hello!")
initialize.init_sqlite_db()
initialize.load_db_to_redis()
scheduler = BackgroundScheduler()
scheduler.add_job(func=utils.activate_meetings, trigger="interval", seconds=4)
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
scheduler.start()


@app.route('/')
def index():
    return render_template('index.html', posts=["Hello"])

# Function: a user joins an active meeting instance – if allowed, i.e. his email is in audience
@app.route('/join_meeting/<meeting_signature>/<user_id>', methods=["GET"])
def join_meeting(meeting_signature, user_id):
    try:
        email = resolve_user_email(user_id)
        # at first we check if a meeting is active
        if cache.sismember("active_meetings", f"meeting:{meeting_signature}"):
            # if a meeting has an audience, then the email should be in the audience set
            if (not cache.exists(f"meeting:{meeting_signature}:audience")) or cache.sismember(f"meeting:{meeting_signature}:audience", email):
                count = cache.get("log_count")
                cache.sadd(f"meeting:{meeting_signature}:joined", user_id)
                cache.hmset(f'log:{count}', {
                "eventID": count,
                "userID": user_id,
                "eventType": "join",
                "timestamp": datetime.now().strftime(r'%d-%m-%Y %H:%M:%S.%f')
                })
                cache.sadd(f"meeting:{meeting_signature}:logs", count)
                cache.incr("log_count")
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
            remove_stmt = cache.srem(f"meeting:{meeting_signature}:joined", user_id)
            count = cache.get("log_count")
            cache.hmset(f'log:{count}', {
                "eventID": count,
                "userID": user_id,
                "eventType": "leave",
                "timestamp": datetime.now().strftime(r'%d-%m-%Y %H:%M:%S.%f')
                })
            cache.incr("log_count")
        except:
            raise(Exception(f"meeting with signature {meeting_signature} is not active!"))
        if remove_stmt:
            return render_template('index.html', posts=[f"Success!"])
        else:
            raise Exception(f"user with email {email} is not found in the audience!")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return render_template('index.html', posts=[f"Error:{str(e)}"])


# Function: show meeting’s current participants
# TODO: Explain we want to print all results
@app.route('/show_meeting_join_timestamps/', methods=["GET"])
def show_meeting_join_timestamps():
    results = []
    try:
        active_meetings = cache.smembers("active_meetings")
        for meeting_signature in active_meetings:
            meeting_signature_json = dict()
            meeting_id = meeting_signature.split(":")[1]
            order_id = meeting_signature.split(":")[2]
            meeting_signature_json["meetingID"] = meeting_id
            meeting_signature_json["orderID"] = order_id
            results.append(meeting_signature_json)
            stmt = cache.smembers(f"{meeting_signature}:logs")
            timestamps = []
            for eventID in stmt:
                timestamps.append(cache.hgetall(f"log:{eventID}"))
            meeting_signature_json["join_info"] = timestamps
        return utils.format_results_dict(results)
            
    except Exception as e:
        return render_template('index.html', posts=[f"Error:{str(e)}"])





# Function: show meeting’s current participants
@app.route('/show_participants/<meeting_signature>', methods=["GET"])
def show_meeting_participants(meeting_signature):
    try:
        stmt = cache.smembers(f"meeting:{meeting_signature}:joined")
        if len(stmt) > 0:
            result = "["
            for user in stmt:
                result += str(cache.hgetall(f"user:{user}")) + ","
            result = result[:-1] + "]"

            return utils.format_results(result)
        else:
            raise Exception(f"meeting is either inactive or does not exist!")
    except Exception as e:
        return render_template('index.html', posts=[f"Error:{str(e)}"])


# Function: show active meetings
@app.route('/show_active_meetings/', methods=["GET"])
def show_active_meetings():
    try:
        stmt = cache.smembers("active_meetings")
        results = []
        if len(stmt) > 0:
            for element in stmt:
                results.append(cache.hgetall(f"{element}"))
            return utils.format_results(results)
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
        if cache.sismember("active_meetings", f"meeting:{meeting_signature}"):
            # if a meeting has an audience, then the email should be in the audience set
            if cache.sismember(f"meeting:{meeting_signature}:joined", user_id):
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
        if cache.sismember("active_meetings", f"meeting:{meeting_signature}"):
            # if a meeting has an audience, then the email should be in the audience set
            result = cache.lrange(f"meeting:{meeting_signature}:messages", 0, -1)
            return utils.format_results_dict(result)
        else:
            raise Exception(f"meeting with signature {meeting_signature} not active!")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return render_template('index.html', posts=[f"Error:{str(e)}"])


@app.route('/get_user_email/<user_id>', methods={"GET"})
def resolve_user_email(user_id):
    result = cache.hmget(f"user:{user_id}", "email")
    if result[0] is None:
        raise Exception("user does not exist")
    return result[0]


# Function: 
@app.route('/show_user_chat/<meeting_signature>/<userID>', methods={"GET"})
def show_user_chat(meeting_signature, userID):
    try:
        if cache.sismember("active_meetings", meeting_signature):
            if cache.sismember(f"meeting:{meeting_signature}:joined"):
                pass
            else:
                raise Exception(f"user not joined in meeting {meeting_signature}!")
            # if a meeting has an audience, then the email should be in the audience set
            result = cache.lrange(f"meeting:{meeting_signature}:messages", 0, -1)
            return render_template('index.html', posts=[f"{result}"])
        else:
            raise Exception(f"meeting with signature {meeting_signature} not active!")
        return render_template('index.html', posts=[f"Success!"])
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return render_template('index.html', posts=[f"Error:{str(e)}"])



def add_event_log(user_id, meeting_signature, type):

    result = cache.hmget(f"user:{user_id}", "email")
    if result[0] is None:
        raise Exception("user does not exist")
    return result[0]
