#!/bin/sh

pid=`ps aux | grep [v]pnc-connect | awk '{print $2}'`

if [ $pid ]
then
  echo $(date +%Y-%m-%d:%T) Connection already established with PID $pid
else
  sudo vpnc-connect rackspace --local-port 0
  echo $(date +%Y-%m-%d:%T) Connection established with PID $pid 
fi

