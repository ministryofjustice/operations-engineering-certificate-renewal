import json
import os
import boto3
from pyaml_env import parse_config

config_location = os.getenv(
    "CONFIG_CONTEXT", default="../configs/production.yml")
config = parse_config(config_location)
file_path = './app/resources/s3_email_mapping.json'

s3 = boto3.client('s3')
with open(file_path, 'wb') as file:
    s3.download_fileobj(config['s3']['s3_bucket_name'], config['s3']['s3_object_name'], file)
    mappings = file.read()

email_map = json.loads(mappings)

print(f"Email map in JSON: {mappings}")

