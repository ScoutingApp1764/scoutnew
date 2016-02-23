while [ "1" = "1" ]
do
	python scoutmaster.py -d
	if [ "$?" = "1" ]; then
		sleep 2
	fi
	sleep 1
done
