## scrape package

* Used to extract data from wikipedia and genius to create the basis for our analysis
* if you want to use it, register with genius and generate an access token, put that into `config.json`
* check if the symlinked `db` directory works for you, is essential for any meaningful usage (otherwise you don't store data)

## Description

* `scrape_wikipedia.py` expects a list of wikipedia in `data/seedfile.csv` links to sites like [List of Hip Hop Musicians](https://en.wikipedia.org/wiki/List_of_hip_hop_musicians). Then writes all contained artist names to stdout.
* `scrape_genius.py` then uses those names to query for the genius IDs of these musicians. Using these IDs, it collects k songs of that artist and writes them to our `SQLite` Database together with a link to the lyrics. 
* `parse_lyrics.py` then downloads those pages and extracts publication year and lyrics from there and updates the databse file.