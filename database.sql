-- Users table.
-- users will be the donors of the website and collaborators
CREATE TABLE IF NOT EXISTS users(
  user_id BIGSERIAL PRIMARY KEY ,
  user_name VARCHAR(16),
  fullname VARCHAR(100),
  email VARCHAR(200),
  password VARCHAR(64),
  phone VARCHAR(20),
  about TEXT,
  extras TEXT
);


--