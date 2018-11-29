# indicate artist here, do not change spaces
artist="beyonce"

# this returns the line numbers where the artist is found in the header
cat lyrics-2.csv | grep -in "^[0-9].*$artist.*" | grep -o "^[0-9]*"

# development:
# further code required to return chunks of lyrics for different artists
# more efficient to do it in shell than in python
# development for calling this within python, possibly through system call
# then creates a new csv with relevant lyrics inside
