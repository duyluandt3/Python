#!/bin/sh

ip link set wmon0 down
iw dev wmon0 del
