#!/bin/sh

if [ $1 = "unittest" ]
then
  export CONFIG_CONTEXT="./configs/test.yml"
  python -m unittest discover -s app/test/ -fv
  exit 0
elif [ $1 = "certexpire" ]
then
  export CONFIG_CONTEXT="./configs/production.yml"
  python3 app/certificate_expiry_check.py
  exit 0
elif [ $1 = "test" ]
then
  export CONFIG_CONTEXT="./configs/production.yml"
  python3 app/test_email.py
  exit 0
else
  echo "Run failed:" >&2
fi



