#!/bin/bash

while [ "1" = "1" ]
do
	echo "Git posted!"
	git add *
	git commit -m "5 minutes passed (gitlazy.sh)"
	git push origin unstable
	sleep 300
done 
