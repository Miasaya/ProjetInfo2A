DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS id_users;
CREATE SEQUENCE id_users_seq;
CREATE TABLE users (
    id_users integer NOT NULL DEFAULT nextval
	('id_users_seq'::regclass) PRIMARY KEY,
	username text,
    mdp text,
    admini boolean);

INSERT INTO users (id_users, username,mdp,admini) VALUES
(1, 'admin','admin',TRUE);