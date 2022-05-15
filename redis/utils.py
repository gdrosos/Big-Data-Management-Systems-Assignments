import json
import sqlite3
import logging
import redis
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    return conn

def get_redis_connection():
    return redis.Redis('localhost', port=6379, decode_responses=True)

cache = get_redis_connection()
conn = get_db_connection()

def activate_meetings():
    print(datetime.now())
    try:
        cursor_obj = conn.cursor()
        current_time = datetime.now()
        meetings = cursor_obj.execute("""
        SELECT m.meetingID, i.orderID, m.title, m.description, m.isPublic, fromdatetime, todatetime
        FROM MEETINGS as m, MEETING_INSTANCES as i
        WHERE m.meetingID = i.meetingID
        """).fetchall()
        for meetingID, orderID, title, description, isPublic, from_dt, to_dt in meetings:
            # print(f">>>>>>>>{meetingID}")
            if "." in from_dt:
                time_string = r'%d-%m-%Y %H:%M:%S.%f'
            else:
                time_string = r'%d-%m-%Y %H:%M:%S'
            start = datetime.strptime(from_dt, time_string)
            end = datetime.strptime(to_dt, time_string)
            meeting_signature = f'meeting:{meetingID}:{orderID}'

            if cache.sismember('active_meetings', meeting_signature):
                if current_time > end:
                    logging.info(f"deactivating meeting {meeting_signature}")
                    cache.srem('active_meetings', meeting_signature)
                    cache.delete(meeting_signature)
                    cache.delete(f'{meeting_signature}:audience')
                    messages = cache.lrange(f'{meeting_signature}:messages', 0, -1)
                    for messageID in messages:
                        cache.delete(f'message:{messageID}')
                    cache.delete(f'{meeting_signature}:messages')

                    # REMOVE JOINED MEMBERS
                    joined = cache.smembers(f'{meeting_signature}:joined')
                    for userID in joined:
                        conn.execute(f"""
                        INSERT INTO EVENTS_LOG (userID, eventType, timestamp)
                        VALUES ({userID}, "leave", '{str(end)}')
                        """)
                    cache.delete(f'{meeting_signature}:joined')


                    # DELETE LOGS
                    logs = cache.lrange(f'{meeting_signature}:logs', 0, -1)
                    for eventID in logs:
                        userID, eventType, timestamp = \
                            cache.hmget(f'log:{eventID}', ["userID", "eventType", "timestamp"])

                        conn.execute(f"""
                        INSERT INTO EVENTS_LOG (userID, eventType, timestamp)
                        VALUES ({userID}, "{eventType}", "{timestamp}")
                        """)

                        cache.delete(f'log:{eventID}')
                    cache.delete(f'{meeting_signature}:logs')
            else:
                if start < current_time < end:
                    logging.info(f"activating meeting {meeting_signature}")
                    cache.sadd('active_meetings', meeting_signature)
                    cache.hmset(meeting_signature, {
                    "title": title,
                    "description": description,
                    "isPublic": isPublic,
                    "fromdatetime": str(start),
                    "todatetime": str(end)
                    })
                    if not isPublic:
                        audience = cursor_obj.execute(f"""
                        SELECT userEmail
                        FROM MEETINGS as m, AUDIENCE as a
                        WHERE m.meetingID = {meetingID}
                        AND m.meetingID = a.meetingID
                        """).fetchall()
                        for email in audience:
                            cache.sadd(f'{meeting_signature}:audience', email[0])
        print("OK")
    except Exception as e:
        print(e)
        print("EXC")

def resolve_user_email(userID):
    result = cache.hmget(f"user:{userID}", "email")
    if result[0] is None:
        raise Exception("user does not exist")
    return result[0]

def format_results(text):
    text = str(text).replace("'",'"')
    parsed = json.loads(text)
    return (json.dumps(parsed, indent=4, sort_keys=True)).replace('\n', '<br>').replace(" ", "&nbsp")