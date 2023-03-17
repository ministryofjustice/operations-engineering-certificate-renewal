#!/bin/sh

if [ $1 = "unittest" ]
then
  export CONFIG_CONTEXT="./configs/test.yml"
  python -m unittest discover -s app/test/ -fv
elif [ $1 = "certexpire" ]
then
  export CONFIG_CONTEXT="./configs/production.yml"
  python3 app/certificate_expiry_check.py
else
  echo "Run failed:" >&2
fi



