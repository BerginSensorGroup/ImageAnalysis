#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/ImageAnalysis
sudo python3 master.py
sudo python3 on_termination.py
cd /
