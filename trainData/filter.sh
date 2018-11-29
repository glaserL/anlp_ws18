# indicate inputs here, do not change spaces
album=".*"
year="[0-9]*"
artist="beyonce"
genre=".*"

# if statements to add ambiguity to defined inputs

if [ "$album" != ".*" ]
then
	album=".*$album.*"
fi

if [ "$artist" != ".*" ]
then
	artist=".*$artist.*"
fi

if [ "$genre" != ".*" ]
then
	genre=".*$genre.*"
fi

# this returns the line numbers where the artist is found in the header
cat lyrics-2.csv | grep -in "^[0-9]*,$album,$year,$artist,$genre,.*" | grep -o "^[0-9]*:[0-9]*"

# development:
# further code required to return chunks of lyrics for different artists
# more efficient to do it in shell than in python
# development for calling this within python, possibly through system call
# then creates a new csv with relevant lyrics inside
