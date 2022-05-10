import sqlite3
from flask import Flask, render_template
import logging
import init
import redis


def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

def get_redis_connection():
    return redis.Redis('localhost')

cache = get_redis_connection()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logging.info("Hello!")
init.init_sqlite_db()
init.load_db_to_redis()
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
