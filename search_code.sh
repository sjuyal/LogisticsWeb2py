#! /bin/bash

if [ ! "$1" ]
then
	echo Usage: `basename $0` Argument
	echo "Example 'bash $0 prime' to search for files containing word prime" 
	exit
fi
echo "List of Files Containing word $1:"
cur=`pwd`
find $cur -type f -name '*' 2> /dev/null | xargs grep $1 2> /dev/null 1> out.txt

cat out.txt | awk -F : '/Binary.*/{next}{print $1}' | uniq 2> /dev/null
rm out.txt



