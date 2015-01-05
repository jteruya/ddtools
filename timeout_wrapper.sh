#!/bin/bash

# ------------------------------------------------------------------------
# timeout_wrapper.sh
#
# Runs a specific shell job for up to N seconds.
# INPUT: <jobname> <maximum seconds to run>
#
# Example: ./timeout_wrapper.sh sleeper10 11
# The above example will run the job "sleeper10" for 11 seconds at max before killing it. 
#
# NOTE: Exclude the ".sh" from the jobname input parameter.
# ------------------------------------------------------------------------

# Get the job and timeout second count from the input
job=$1
MaxSeconds=$2
emailaddress=$3

emailheader="To: ${emailaddress}
From: \"Timeout Wrapper\" <${emailaddress}>
Subject: TIMEOUT ALERT: The job ${job} took longer than ${MaxSeconds} seconds and was terminated. <EOM>
Content-Type: text/html
"

echo "Running the ${job} job for up to ${MaxSeconds} seconds."

( ./$job.sh ) & pid=$!
( sleep $MaxSeconds && kill -HUP $pid ) 2>/dev/null & watcher=$!
if wait $pid 2>/dev/null; then
    echo "${job} finished."
    pkill -HUP -P $watcher
    wait $watcher
else
    echo "${job} took longer than ${MaxSeconds} seconds."

    # Send email about the job taking too long.
    echo -e "$emailheader" | sendmail -t

fi