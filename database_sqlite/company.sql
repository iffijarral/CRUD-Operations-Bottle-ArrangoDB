DROP TABLE IF EXISTS users;
 
CREATE TABLE users(
    user_pk         TEXT,
    user_name       TEXT,    
    user_email      TEXT UNIQUE,
    user_password   TEXT,
    user_created_at INTEGER,
    user_updated_at TEXT, 
    PRIMARY KEY(user_pk)
) WITHOUT ROWID;

-- Seed users
INSERT INTO users VALUES("1", "One", "one@one.com", "password", "0");

SELECT * FROM users;