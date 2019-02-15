-- songs table
CREATE TABLE IF NOT EXISTS songs (
 id INTEGER PRIMARY KEY,
 title TEXT NOT NULL,
 artist TEXT NOT NULL,
 year TEXT,
 genre TEXT,
 genius_url TEXT,
 lyrics TEXT,
 language TEXT,
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
    id INTEGER PRIMARY KEY,
    artist TEXT NOT NULL,
    wikipedia_url TEXT NOT NULL,
    genius_id INTEGER,
    genius_url TEXT,
    genre TEXT
)