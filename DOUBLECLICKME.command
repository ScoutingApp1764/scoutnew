#!/bin/bash
#./scout/scout.py &
echo ${0%D*d}
cd ${0%D*d}
echo PLEASE CLICK ON THE APPLICATION THAT POPPED UP OR CLICK ON PYTHON IN THE DOCK.
if [ ! -d "FlaskExists" ]; then
    easy_install --user flask
    easy_install --user sqlalchemy
    mkdir FlaskExists
fi

killall python #kill the server if it was started
./scoutmaster.py &
sleep 4
cd /
killall firefox # kill firefox if it was started
./Applications/Firefox.app/Contents/MacOS/firefox 127.0.0.1:9001 &

