#!/bin/sh

rfkill unblock all
rfkill list
iwconfig
sudo ip link set wlp5s0 down
iw dev wlp5s0 interface add wmon0 type monitor
ip link set wmon0 up
sudo iw dev wlp5s0 del
iwconfig
echo "---------------------------------------"
echo "Example --> iw dev wmon0 set channel 10"
echo "Please start Wireshark for Air-capture!"
echo "---------------------------------------"
