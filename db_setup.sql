CREATE TYPE job_status AS ENUM ('new', 'initializing', 'initialized', 'running', 'success', 'error');

CREATE TABLE jobs(
	id SERIAL, 
	client_id varchar(256), 
	status job_status, 
	status_change_time timestamp
);

CREATE OR REPLACE FUNCTION jobs_status_notify()
	RETURNS trigger AS
$$
BEGIN
	PERFORM pg_notify('jobs_status_channel', NEW.id::text);
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER jobs_status
	AFTER INSERT OR UPDATE OF status
	ON jobs
	FOR EACH ROW
EXECUTE PROCEDURE jobs_status_notify();
