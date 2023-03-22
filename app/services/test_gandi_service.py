import datetime
import unittest

from freezegun import freeze_time
from pyaml_env import parse_config

from app.services.GandiService import GandiService


# @patch('requests.get')
# class TestGandiServiceGetExpiredCertificates(unittest.TestCase):
#     #TODO

@freeze_time("2023-02-01")
class TestGetExpiredCertificates(unittest.TestCase):
    def setUp(self):
        self.config = parse_config('../../configs/test.yml')
        self.test_domain_name = 'test.domain.gov.uk'

    def test_valid_certificate_list_returns_expected_domain(self):
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)

        test_data = {
            "test_list": {
                self.test_domain_name: {
                    "recipient": "test.user@mail.com",
                    "recipientcc": [],
                    "owner": "OE",
                    "external_cname": ["external.person@mail.com"]
                }
            },
            'test_certificate_list': {
                self.test_domain_name: {
                    'expiry_date': expiry_date
                }
            }
        }

        response = GandiService(self.config, 'api_key', 'base_url', 'url_ext') \
            .get_expired_certificates_from_valid_certificate_list(
            test_data['test_certificate_list'],
            test_data['test_list'])

        print(f"Response: {response}")
        self.assertIn(self.test_domain_name, response)


if __name__ == '__main__':
    unittest.main()
