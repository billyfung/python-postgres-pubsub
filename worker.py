import select
import os

import psycopg2
import psycopg2.extensions

db = os.getenv("DB_NAME")
dbuser = os.getenv("DB_USER")
dbpass = os.getenv("DB_PASS")
dbhost = os.getenv("DB_HOST")

conn = psycopg2.connect(dbname=db, user=dbuser, password=dbpass, host=dbhost)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

curs = conn.cursor()
curs.execute("LISTEN jobs_status_channel;")

print(f'listening to jobs_status_channel {db}@{dbhost}')
while True:
    if select.select([conn],[],[],5) == ([],[],[]):
        print("Timeout")
    else:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print(f"Got NOTIFY: {notify.pid} {notify.channel} {notify.payload}")
