import unittest
from unittest.mock import patch
import datetime
from scripts import certificate_expiry_check
import test_utilities


class TestCertificateExpiryCheck(unittest.TestCase):

    @patch('config.GANDI_API_KEY', "xxx")
    @patch('config.NOTIFY_API_KEY', "xxx")
    @patch('requests.get')
    @patch('scripts.certificate_expiry_check.build_params')
    @patch('scripts.certificate_expiry_check.send_email')
    def test_email_is_sent_when_expected(self, mock_send_email, mock_build_params, mock_get):

        delta = (datetime.datetime.today() +
                 datetime.timedelta(days=30)).date()
        test_expiry_date = str(
            delta.year) + "-" + str(delta.month) + "-" + str(delta.day) + "T06:00:00Z"

        test_data = {
            "test_list": {
                'test.domain.gov.uk': {
                    "recipient": "test_user@mail.com",
                    "recipientcc": "",
                    "owner": "OE",
                    "external_cname": []
                }
            },
            "mock_send_email_response": {
                "response": "mock_response",
            },
            "mock_build_params_response": {
                "response": "mock_response"
            },
            "mock_gandi_response": [{
                "cn": "test.domain.gov.uk",
                "status": "valid",
                "dates": {
                    "ends_at": test_expiry_date
                }
            }]
        }

        mock_resp = test_utilities._mock_response(
            json_data=test_data['mock_gandi_response'])
        mock_get.return_value = mock_resp
        mock_send_email.return_value(test_data['mock_send_email_response'])
        mock_build_params.return_value(test_data['mock_build_params_response'])

        certificate_expiry_check.find_expiring_certificates(
            test_data['test_list'])

        mock_send_email.assert_called_once()
        mock_build_params.assert_called_once()

    @patch('config.GANDI_API_KEY', "xxx")
    @patch('config.NOTIFY_API_KEY', "xxx")
    @patch('requests.get')
    @patch('scripts.certificate_expiry_check.build_params')
    @patch('scripts.certificate_expiry_check.send_email')
    def test_email_is_not_sent_when_expected(self, mock_send_email, mock_build_params, mock_get):

        delta = (datetime.datetime.today() +
                 datetime.timedelta(days=50)).date()
        test_expiry_date = str(
            delta.year) + "-" + str(delta.month) + "-" + str(delta.day) + "T06:00:00Z"

        test_data = {
            "test_list": {
                'test.domain.gov.uk': {
                    "recipient": "test_user@mail.com",
                    "recipientcc": "",
                    "owner": "OE",
                    "external_cname": []
                }
            },
            "mock_send_email_response": {
                "response": "mock_response",
            },
            "mock_build_params_response": {
                "response": "mock_response"
            },
            "mock_gandi_response": [{
                "cn": "test.domain.gov.uk",
                "status": "valid",
                "dates": {
                    "ends_at": test_expiry_date
                }
            }]
        }

        mock_resp = test_utilities._mock_response(
            json_data=test_data['mock_gandi_response'])
        mock_get.return_value = mock_resp
        mock_send_email.return_value(test_data['mock_send_email_response'])
        mock_build_params.return_value(test_data['mock_build_params_response'])

        certificate_expiry_check.find_expiring_certificates(
            test_data['test_list'])

        mock_send_email.assert_not_called()
        mock_build_params.assert_not_called()


if __name__ == '__main__':
    unittest.main()
