import json
import unittest
from unittest.mock import MagicMock, patch

from app.services.S3Service import S3Service


@patch('boto3.client')
class TestS3ServiceInnit(unittest.TestCase):

    def test_sets_up_class(self, mock_s3: MagicMock):
        mock_s3.return_value = "test_value"
        s3Service = S3Service()
        self.assertEqual(s3Service.client, "test_value")


@patch('boto3.client', new=MagicMock())
@patch('builtins.open')
class TestS3ServiceGetFile(unittest.TestCase):

    def test_returns_file_when_file_contains_json(self, mock_open: MagicMock):
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({"test": "json"})
        response = S3Service().get_json_file("", "", "")
        self.assertEqual(response, {"test": "json"})

    def test_returns_value_error_when_file_does_not_contain_json(self, mock_open: MagicMock):
        mock_open.return_value.__enter__.return_value.read.return_value = "not_json"
        s3Service = S3Service()
        self.assertRaises(ValueError, s3Service.get_json_file, "", "", "")


if __name__ == '__main__':
    unittest.main()
