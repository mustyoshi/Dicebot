#!/bin/bash
killall skype
killall rng.py
sleep 5
while :
do
skype&
sleep 10
(./rng.py)&
sleep 30800
killall skype
killall rng.py
sleep 3
done