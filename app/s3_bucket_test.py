import os
import boto3
from pyaml_env import parse_config

config_location = os.getenv(
    "CONFIG_CONTEXT", default="../configs/production.yml")
config = parse_config(config_location)
file_path = './app/resources/s3_email_mapping.json'

# file_path = os.path.join(os.getcwd(), 'resources', 'mappings.json')

s3 = boto3.client('s3')
# s3.download_file('operations-engineering-certificate-email', 'mappings.json', file_path)

with open(file_path, 'wb') as file:
    s3.download_fileobj('operations-engineering-certificate-email', 'mappings.json', file)

with open(file_path) as my_file:
    print(my_file.read())

# resources_dir = os.path.join(os.getcwd(), 'resources')
# for root, dir, files in os.walk(resources_dir):
#     for filename in files:
#         print(f"Filename: {filename}")
