#!/bin/sh

if [ $1 = "unittest" ]
then
  export CONFIG_CONTEXT="./configs/test.yml"
  python -m unittest discover -s app/test/ -fv
  exit 0
elif [ $1 = "testrun" ]
# This is a temporary option for testing
then
  export CONFIG_CONTEXT="./configs/production.yml"
  python3 app/send_email_test.py
  exit 0
elif [ $1 = "s3test" ]
# This is a temporary option for testing s3 interactions
then
  export CONFIG_CONTEXT="./configs/production.yml"
  python3 app/s3_bucket_test.py
  exit 0
elif [ $1 = "certexpire" ]
then
  export CONFIG_CONTEXT="./configs/production.yml"
  python3 app/certificate_expiry_check.py
  exit 0
else
  echo "Run failed:" >&2
fi



