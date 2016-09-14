./start.bash
ps 
./stop.bash
echo "##############################################################################"
echo "RESTARTING SERVICES, then kill 1 to see if systemd restarts it automatically"
sleep 1
./start.bash
echo "##############################################################################"
ps -aux | grep "x" | grep "test.bash"
echo "##############################################################################"
echo "KILL x1"
ps -aux | grep "x1" | grep "test.bash" | awk '{print $2}' | xargs kill -9
ps -aux | grep "x" | grep "test.bash"
echo "##############################################################################"
sleep 1
ps -aux | grep "x" | grep "test.bash"
./status.bash
sleep 1
echo "##############################################################################"
echo "KILL x1"
ps -aux | grep "x1" | grep "test.bash" | awk '{print $2}' | xargs kill -9
echo "##############################################################################"
./status.bash
sleep 3
./status.bash
echo "##############################################################################"
./stop.bash
echo "STOPPING all"
sleep 1
echo "##############################################################################"
./status.bash

