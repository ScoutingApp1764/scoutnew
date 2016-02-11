#!/bin/bash

while [ "1" = "1" ]
do
	echo "Git posted!"
	git add *
	git commit -m "5 minutes passed (gitlazy.sh)"
	let mins =5
	let "secs = $mins * 60"
	sleep $secs
done 
