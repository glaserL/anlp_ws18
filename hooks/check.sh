#!/bin/bash
set -e

# work on root
cd ..

# find modules imported via "import" or "from"
a=$(grep -r -E --include=\*.py '^import' ./ | cut -d" " -f2 | cut -d "," -f1 | sort | uniq)
b=$(grep -r -E --include=\*.py '^from .* import .*' ./ | cut -d" " -f2 | cut -d "," -f1 | sort | uniq)

# combine modules
c="${a}\n${b}"

# find root modules in case submodules were called
d=$(echo -e "$c" | cut -d "." -f1 | sort | uniq)

# find .py files and directories which could be part of imported modules
e=$(find -name '*.py' -printf '%h\n' | sort -u | grep -oE '[^/]+$')
f=$(find -name '*.py' | sort -u | grep -oE '[^/]+$' | sed 's/.py//g')

# write unwanted files to exclude.txt
echo "$e" > ./hooks/exclude.txt
echo "$f" >> ./hooks/exclude.txt

# exclude unwanted files and write to requirements.txt
echo "$d" | grep -vf ./hooks/exclude.txt > requirements.txt
