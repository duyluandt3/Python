#!/bin/sh

set -eu

sudo python3 chk_wmon.py

sudo ip link set wlp4s0 down

sudo iw dev wlp4s0 interface add wmon0 type monitor

sudo ip link set wmon0 up

sudo iw dev wlp4s0 del


