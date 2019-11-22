# Postgres Asynchronous Notification
This is just for playing around with Postgres functionality of LISTEN and NOTIFY
https://www.postgresql.org/docs/12/libpq-notify.html

Beats having to set up another application if already using Postgres as the backend.

# Set up
```
docker-compose up
```

Postgres db with a table `jobs` 
Python process that checks `jobs_status_channel` on Postgres

When both are running, insert into the table jobs to get a notification in the python worker. 

```
insert into jobs(client_id, status, status_change_time) values ('45', 'new', now())
```

The worker will then pick up the notification.
```
worker    | listening to jobs_status_channel testdb@db
worker    | Timeout
worker    | Got NOTIFY: 45 jobs_status_channel 7
worker    | Timeout
```