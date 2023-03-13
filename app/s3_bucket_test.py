import os
import boto3
from pyaml_env import parse_config

config_location = os.getenv(
    "CONFIG_CONTEXT", default="../configs/production.yml")
config = parse_config(config_location)
file_path = './app/resources/s3_email_mapping.json'

s3 = boto3.client('s3')
s3.download_file(config.get(
    config['s3']['bucket_name']), config['s3']['object_name'], file_path)