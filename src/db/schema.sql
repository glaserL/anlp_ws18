-- songs table
CREATE TABLE IF NOT EXISTS songs (
 id integer PRIMARY KEY,
 title text NOT NULL,
 artist text NOT NULL,
 year text,
 genre text,
 genius_url text,
 lyrics text,
 postagged TEXT,
 lemmatized TEXT,
 frequency TEXT,
 sentiment REAL,
 avg_word_length REAL,
 non_std_words REAL,
 ttr REAL,
 lexical_density REAL
);

CREATE TABLE IF NOT EXISTS scrape (
    id integer PRIMARY KEY,
    artist text NOT NULL,
    wikipedia_url text NOT NULL,
    genius_id integer,
    genius_url text
)