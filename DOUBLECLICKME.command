#!/bin/bash
#./scout/scout.py &
echo ${0%D*d}
cd ${0%D*d}
#just run firefox
if [ $2 ]; then
    sleep 2
    cd /
    killall firefox # kill firefox if it was started
    ./Applications/Firefox.app/Contents/MacOS/firefox 127.0.0.1:9001 &
#double fork
elif [ $1 ]; then
    echo running...
    if [ ! -d "FlaskExists" ]; then
        easy_install --user flask
        yes | ./scoutmaster.py -c
        #^^pipe yes to confirm to clear the database, just in case i forgot to do so before git commiting
        mkdir FlaskExists
    fi
    ./DOUBLECLICKME.command these arguementsdontmatter &
    killall python #kill the server if it was started
    python scoutmaster.py 
   else 
    echo forking...
    ./DOUBLECLICKME.command forked &
    sleep 99999999999999999999999999999999999999999999 #when your script goes from bodge to hack
fi
