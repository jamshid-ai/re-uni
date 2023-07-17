import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv('HOST'),
    database=os.getenv('DATABASE'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS')
)


def create_user(first_name, last_name, tg_id):
    curr = conn.cursor()
    curr.execute(
        "INSERT INTO contact (first_name, last_name, tg_id) VALUES(%s, %s, %s)", (first_name, last_name, tg_id))
    conn.commit()
    curr.close()


def get_user(tg_id):
    curr = conn.cursor()
    curr.execute("SELECT * FROM contact WHERE tg_id=%s", (tg_id,))
    return curr.fetchall()
