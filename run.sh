#!/bin/sh

if [ $1 = "unittest" ]
then
  python -m unittest discover -s test/ -fv

elif [ $1 = "certexpire" ]
then
  export CONFIG_CONTEXT="./configs/production.yml"
  python3 app/jobs/certificate_expiry_check.py
elif [ $1 = "testrun" ]
then
  export CONFIG_CONTEXT="./configs/production.yml"
  python3 app/jobs/certificate_expiry_check.py -test $2
else
  echo "Run failed:" >&2
fi
