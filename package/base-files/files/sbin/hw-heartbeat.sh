#!/bin/sh
# /sbin/hw-heartbeat.sh
#  send heartbeat to the hardware watchdog 

GPO="3"

gpioctl dirout $GPO
gpioctl clear $GPO
sleep 1
gpioctl set $GPO
logger -st ${0##*/} "signaling to the hw-watchdog"
