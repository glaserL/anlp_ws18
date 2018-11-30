#!/bin/bash

# indicate inputs here, do not change spaces
# can indicate possibilities using regex special character "|"
# default should be ".*" to maintain ambiguity, inputs are regex characters
song=".*"
year="[0-9]*"
artist="beyonce"
genre=".*"

# if statements to add ambiguity to defined inputs
# eg. "beyonce" should also return "Beyonce-Knowles"
if [ "$song" != ".*" ]
then
	song=".*$song.*"
fi

if [ "$artist" != ".*" ]
then
	artist=".*$artist.*"
fi

if [ "$genre" != ".*" ]
then
	genre=".*$genre.*"
fi

# this returns the line numbers where the inputs are found in the header
# these line numbers can be utilized to extract specific portions of lyrics
lines=$(cat lyrics-2.csv | grep -inE "^[0-9]*,$song,$year,$artist,$genre,.*" | grep -o "^[0-9]*:[0-9]*")

lines2=$(echo "$lines" | grep -oE "[0-9]*$")

# code adapted from https://stackoverflow.com/questions/44510813/changing-the-field-separator-of-awk-to-newline

linesShortened=$(awk -F " " '{
                r = nxt = 0;
                for (i=1; i<=NF; i++)
                    if ($i+1 == $(i+1)){ if (!r) r = $i"-"; nxt = $(i+1) } 
                    else { printf "%s%s", (r)? r nxt : $i, (i == NF)? ORS : FS; r = 0 }
           }' <<<$lines2)

len=$(awk -F" " 'NF{print NF-1}' <<< $linesShortened)

for i in `seq $((len + 1))`
do
	range=$(echo "$linesShortened" | cut -d " " -f $i)
	if [[ "$range" =~ "-" ]]; then
		for j in `seq 2`
		do
			indices=$(echo "$lines" | grep -E ":$(echo $range | cut -d '-' -f $j)$" | grep -oE "^[0-9]*")
			if [ $j -eq 1 ] 
			then
				start=$indices
			else
				end=$indices
			fi
		done
	sed -n "$start,${end}p;${end}q" lyrics-2.csv > extract$i.txt
	fi
done

# development:

# handle individual tags which can be problematic
# further code required to return chunks of lyrics for different artists
# more efficient to do it in shell than in python
# call this within python through system call
# then creates a new csv with relevant lyrics inside
# shorter lyrics can then be directly processed in python
# side task if we want specific output and not ambiguated
