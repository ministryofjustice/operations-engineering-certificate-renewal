import json
from json import JSONDecodeError

import boto3


class S3Service:
    def __init__(self) -> None:
        self.client = boto3.client('s3')

    def get_json_file(self, bucket_name: str, object_name: str, file_path: str):
        with open(file_path, 'wb') as file:
            self.client.download_fileobj(bucket_name, object_name, file)
        with open(file_path) as file:
            mappings = file.read()

        try:
            return json.loads(mappings)
        except JSONDecodeError as e:
            raise ValueError("File not in JSON Format") from e
