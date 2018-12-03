#!/bin/bash

# information on utility of function
usage() {
	echo "Usage: $0 [-b base-file] [-d destination-file] ..."
	echo
	echo "Mandatory Arguments:"
	echo "  -b      base-file"
	echo "  -d      destination-file"
	echo "Optional Arguments":
	echo "  -s      song (regex)"
	echo "  -y      year (regex)"
	echo "  -a      artist (regex)"
	echo "  -g      genre (regex)"
	echo "  -t      search for exact string matches"
	echo "  -v      print entire vocabulary of data"
	1>&2
	exit 1;
}

# indicate inputs here, do not change spaces
# default should be ".*" to maintain ambiguity, inputs are regex characters
song=".*"
year="[0-9]*"
artist=".*"
genre=".*"
t="0"

while getopts ":b:d:s:y:a:g:thv" option; do
	case $option in
	b)
		if [ "x" == "x$OPTARG" ]; then
			usage
			exit 1
		else
			base=$OPTARG
		fi
	;;
	d)
		if [ "x" == "x$OPTARG" ]; then
			usage
			exit 1
		else
			dest=$OPTARG
			if [ -e "$dest" ]; then
				rm "$dest"
			fi
		fi
	;;
	s)
		if [ "x" != "x$OPTARG" ]; then
			song=$OPTARG
		fi
	;;
	y)
		if [ "x" != "x$OPTARG" ]; then
			year=$OPTARG
		fi
	;;
	a)
		if [ "x" != "x$OPTARG" ]; then
			artist=$OPTARG
		fi
	;;
	g)
		if [ "x" != "x$OPTARG" ]; then
			genre=$OPTARG
		fi
	;;
	t)
		t="1"
	;;
	v)
		if [ "x" != "x$base" ] && [ "x" != "x$dest" ]; then
			cat $base | grep "^[0-9]*," >> $dest
			exit 0
		else
			usage
			exit 1
		fi
	;;
	h) usage
	;;
	\?) usage
	;;
	*) usage
	;;
	esac
done

# remove non-alphanumerics and replace with dash
# make actions based on looseness or tightness
if [ "$song" != ".*" ]
then
	song=$(echo "$song" | sed 's/[^a-zA-Z0-9]/-/g')
	if [[ $t -eq 0 ]]; then
		song=".*$song.*"
	fi
fi

if [ "$artist" != ".*" ]
then
	artist=$(echo "$artist" | sed 's/[^a-zA-Z0-9]/-/g')
	if [[ $t -eq 0 ]]; then
		artist=".*$artist.*"
	fi
fi

if [ "$genre" != ".*" ]
then
	genre=$(echo "$genre" | sed 's/[^a-zA-Z0-9]/-/g')
	if [[ $t -eq 0 ]]; then
		genre=".*$genre.*"
	fi
fi

# this returns the line numbers where the inputs are found in the header
# these line numbers can be utilized to extract specific portions of lyrics
lines=$(cat $base | grep -inE "^[0-9]*,$song,$year,$artist,$genre,.*" | grep -o "^[0-9]*:[0-9]*")
lines2=$(echo "$lines" | grep -oE "[0-9]*$")

# code adapted from https://stackoverflow.com/questions/44510813/changing-the-field-separator-of-awk-to-newline
linesShortened=$(gawk -F " " '{
                r = nxt = 0;
                for (i=1; i<=NF; i++)
                    if ($i+1 == $(i+1)){ if (!r) r = $i"-"; nxt = $(i+1) }
                    else { printf "%s%s", (r)? r nxt : $i, (i == NF)? ORS : FS; r = 0 }
           }' <<<$lines2)

len=$(gawk -F" " 'NF{print NF-1}' <<< $linesShortened)

for i in `seq $((len + 1))`
do
	range=$(echo "$linesShortened" | cut -d " " -f $i)
	# in case of ranges, can process in batches here
	if [[ "$range" =~ "-" ]]; then
		for j in `seq 2`
		do
			if [ $j -eq 1 ];then
				start=$(echo "$lines" | grep -E ":$(echo $range | cut -d '-' -f $j)$" | grep -oE "^[0-9]*")
			else
				end=$(cat $base | grep -oEn "^$(($(echo $range | cut -d '-' -f $j) + 1))," | grep -oE "^[0-9]*")
				end="$(($end - 1 ))"
			fi
		done
		sed -n "$start,${end}p;${end}q" $base >> $dest
	else
	
	# in case of single entities, can process individually here
		start=$(echo "$lines" | grep -E ":$range$" | grep -oE "^[0-9]*")
		end=$(cat $base | grep -oEn "^$(($range + 1))," | grep -oE "^[0-9]*")
		len2=$(gawk -F" " 'NF{print NF-1}' <<< $start)
		len3=$(gawk -F" " 'NF{print NF-1}' <<< $end)
		if [ $len2 -gt 1 ] || [ $len3 -gt 1 ]; then
			start=$(echo $start | cut -d " " -f 1)
			end=$(echo $end | cut -d " " -f 1)
		fi
		end="$(($end - 1 ))"
		sed -n "$start,${end}p;${end}q" $base >> $dest
	fi
done

exit 0
