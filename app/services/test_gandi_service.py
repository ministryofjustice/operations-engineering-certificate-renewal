import datetime
import unittest
from unittest.mock import MagicMock, patch

from pyaml_env import parse_config

from app.services.GandiService import GandiService


@patch('requests.get')
class TestGandiServiceGetExpiredCertificates(unittest.TestCase):

    def setUp(self):
        self.config = parse_config('../../configs/test.yml')
        self.test_domain_name = 'test.domain.gov.uk'

    def test_returns_correct_certificates(self, mock_request: MagicMock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "cn": self.test_domain_name,
            "status": "valid",
            "dates": {
                "ends_at": self.set_gandi_date_format(True)
            }
        }]

        test_email_list = {
            self.test_domain_name: {
                "recipient": "test.user@mail.com",
                "recipientcc": [],
                "owner": "OE",
                "external_cname": []
            }
        }

        mock_request.return_value = mock_response
        response = GandiService(self.config).get_expiring_certificates(test_email_list)

        self.assertIn(self.test_domain_name, response)

    def test_returns_multiple_correct_certificates(self, mock_request: MagicMock):
        test_another_domain_name = 'test.another.domain.name'

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "cn": self.test_domain_name,
            "status": "valid",
            "dates": {
                "ends_at": self.set_gandi_date_format(True)
            }
        },
            {
                "cn": test_another_domain_name,
                "status": "valid",
                "dates": {
                    "ends_at": self.set_gandi_date_format(True)
                }
            },
        ]

        test_email_list = {
            self.test_domain_name: {
                "recipient": "test.user@mail.com",
                "recipientcc": [],
                "owner": "OE",
                "external_cname": []
            },
            test_another_domain_name: {
                "recipient": "test.another.user@mail.com",
                "recipientcc": [],
                "owner": "OE",
                "external_cname": []
            }
        }

        mock_request.return_value = mock_response
        response = GandiService(self.config).get_expiring_certificates(test_email_list)

        self.assertIn(self.test_domain_name, response)
        self.assertIn(test_another_domain_name, response)

    def test_returns_multiple_correct_emails(self, mock_request: MagicMock):
        test_email = 'test.user@mail.com'
        test_cc_mail = 'test.cc.user@mail.com'
        test_another_cc_mail = 'test.another.cc.user@mail.com'

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "cn": self.test_domain_name,
            "status": "valid",
            "dates": {
                "ends_at": self.set_gandi_date_format(True)
            }
        }]

        test_email_list = {
            self.test_domain_name: {
                "recipient": test_email,
                "recipientcc": [
                    test_cc_mail,
                    test_another_cc_mail
                ],
                "owner": "OE",
                "external_cname": []
            }
        }

        mock_request.return_value = mock_response
        response = GandiService(self.config).get_expiring_certificates(test_email_list)

        self.assertIn(test_email, response[self.test_domain_name]['emails'])
        self.assertIn(test_cc_mail, response[self.test_domain_name]['emails'])
        self.assertIn(test_another_cc_mail, response[self.test_domain_name]['emails'])


    def test_does_not_return_certificate_with_invalid_status(self, mock_request: MagicMock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "cn": self.test_domain_name,
            "status": "pending",
            "dates": {
                "ends_at": self.set_gandi_date_format(True)
            }
        }]

        test_email_list = {
            self.test_domain_name: {
                "recipient": "test.user@mail.com",
                "recipientcc": [],
                "owner": "OE",
                "external_cname": []
            }
        }

        mock_request.return_value = mock_response
        response = GandiService(self.config).get_expiring_certificates(test_email_list)

        self.assertNotIn(self.test_domain_name, response)

    def test_does_not_return_certificate_with_invalid_date(self, mock_request: MagicMock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "cn": self.test_domain_name,
            "status": "valid",
            "dates": {
                "ends_at": self.set_gandi_date_format(False)
            }
        }]

        test_email_list = {
            self.test_domain_name: {
                "recipient": "test.user@mail.com",
                "recipientcc": [],
                "owner": "OE",
                "external_cname": []
            }
        }

        mock_request.return_value = mock_response
        response = GandiService(self.config).get_expiring_certificates(test_email_list)

        self.assertNotIn(self.test_domain_name, response)

    def test_returns_external_cname_if_present(self, mock_request: MagicMock):
        test_cname_user = 'cname.user@mail.com'

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "cn": self.test_domain_name,
            "status": "valid",
            "dates": {
                "ends_at": self.set_gandi_date_format(True)
            }
        }]

        test_email_list = {
            self.test_domain_name: {
                "recipient": "test.user@mail.com",
                "recipientcc": [],
                "owner": "OE",
                "external_cname": [
                    test_cname_user
                ]
            }
        }

        mock_request.return_value = mock_response
        response = GandiService(self.config).get_expiring_certificates(test_email_list)

        self.assertIn(test_cname_user, response[self.test_domain_name]['emails'])

    def test_returns_multiple_external_cname_if_present(self, mock_request: MagicMock):
        test_cname_user = 'cname.user@mail.com'
        test_another_cname_user = 'another.cname.user@mail.com'

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "cn": self.test_domain_name,
            "status": "valid",
            "dates": {
                "ends_at": self.set_gandi_date_format(True)
            }
        }]

        test_email_list = {
            self.test_domain_name: {
                "recipient": "test.user@mail.com",
                "recipientcc": [],
                "owner": "OE",
                "external_cname": [
                    test_cname_user,
                    test_another_cname_user
                ]
            }
        }

        mock_request.return_value = mock_response
        response = GandiService(self.config).get_expiring_certificates(test_email_list)

        self.assertIn(test_cname_user, response[self.test_domain_name]['emails'])
        self.assertIn(test_another_cname_user, response[self.test_domain_name]['emails'])

    def set_gandi_date_format(self, valid: bool) -> str:
        future_days = self.config['cert_expiry_thresholds'][0] + 20
        if valid:
            future_days = self.config['cert_expiry_thresholds'][0]
        delta = (datetime.datetime.today() +
                 datetime.timedelta(days=future_days)).date()
        test_expiry_date = str(
            delta.year) + "-" + str(delta.month) + "-" + str(delta.day) + "T06:00:00Z"
        return test_expiry_date


if __name__ == '__main__':
    unittest.main()

