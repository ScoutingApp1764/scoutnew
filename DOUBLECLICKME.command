#!/bin/bash
#./scout/scout.py &
echo ${0%D*d}
cd ${0%D*d}
./scoutmaster.py &
echo PLEASE CLICK ON THE APPLICATION THAT POPPED UP OR CLICK ON PYTHON IN THE DOCK.
