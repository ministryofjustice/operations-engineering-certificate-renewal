import unittest

from freezegun import freeze_time

from app.services.GandiService import GandiService
from test.resources.test_data import TestData
from test.test_config import test_config


@freeze_time("2023-01-01")
class TestGetExpiredCertificates(unittest.TestCase):
    def test_valid_certificate_list_returns_expected_domain(self):
        response = GandiService(test_config, 'api_key', 'base_url', 'url_ext') \
            .get_expired_certificates_from_valid_certificate_list(
            TestData.generate_filtered_certificate_list_with_expiry_date(30),
            TestData.generate_valid_email_list())
        self.assertIn(TestData.test_domain_name, response)


@freeze_time("2023-01-01")
class TestValidCertificateRetrieval(unittest.TestCase):
    def test_only_valid_certificates_are_returned_from_list(self):
        response = GandiService(test_config, 'api_key', 'base_url', 'url_ext') \
            .get_certificates_in_valid_state(
            TestData.generate_gandi_certificate_date('valid'),
            TestData.generate_valid_email_list()
        )

        self.assertIn(TestData.test_domain_name, response)


if __name__ == '__main__':
    unittest.main()
