-- songs table
CREATE TABLE IF NOT EXISTS songs (
 id integer PRIMARY KEY,
 song text NOT NULL,
 artist text NOT NULL,
 year text,
 genre text,
 lyrics text
);
