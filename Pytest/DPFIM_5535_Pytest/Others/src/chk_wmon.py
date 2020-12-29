import os
import subprocess as sub
import time

com  = sub.getoutput('iwconfig wmon0')
nothing  = "No such device"

if com.find(nothing) == -1:
  sub.call('sudo iw wmon0 set freq 5240 40 5250',shell=True)
  while com.find(nothing) == -1:
    time.sleep(2)
    com  = sub.getoutput('iwconfig wmon0')
