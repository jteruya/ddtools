#!/bin/sh

echo started | mail -s $1 anguyen@doubledutch.me

python /home/anguyen/tools/get_csv.py $1

cat `pwd`/nohup.out | mail -s $1 anguyen@doubledutch.me

