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
            TestData.generate_single_email_list())
        
        self.assertIn(TestData.test_domain_name_root, response)


@freeze_time("2023-01-01")
class TestCertificateRetrievalValidity(unittest.TestCase):
    def test_only_valid_certificates_are_returned_from_list(self):
        response = GandiService(test_config, 'api_key', 'base_url', 'url_ext') \
            .get_certificates_in_valid_state(
            TestData.generate_single_gandi_certificate_state('valid'),
            TestData.generate_single_email_list()
        )

        self.assertIn(TestData.test_domain_name_root, response)

    def test_invalid_certificate_is_not_returned(self):
        response = GandiService(test_config, 'api_key', 'base_url', 'url_ext') \
            .get_certificates_in_valid_state(
            TestData.generate_single_gandi_certificate_state('pending'),
            TestData.generate_single_email_list()
        )

        self.assertNotIn(TestData.test_domain_name_root, response)

    def test_multiple_valid_certificates_returned(self):
        test_case_count = 3
        response = GandiService(test_config, 'api_key', 'base_url', 'url_ext') \
            .get_certificates_in_valid_state(
            TestData.generate_multiple_gandi_certificate_states(
                'valid', test_case_count),
            TestData.generate_multiple_email_list(test_case_count)
        )

        self.assertIn(f"{TestData.test_domain_name_root}0", response)
        self.assertIn(f"{TestData.test_domain_name_root}1", response)
        self.assertIn(f"{TestData.test_domain_name_root}2", response)

    def test_only_valid_certificate_is_returned(self):
        test_case_count = 3
        test_cases = TestData.generate_multiple_gandi_certificate_states(
            'pending', test_case_count)
        test_cases += TestData.generate_single_gandi_certificate_state('valid')
        test_email_list = TestData.generate_multiple_email_list(
            test_case_count)
        test_email_list.update(TestData.generate_single_email_list())

        response = GandiService(test_config, 'api_key', 'base_url', 'url_ext') \
            .get_certificates_in_valid_state(
            test_cases,
            test_email_list
        )

        self.assertNotIn(f"{TestData.test_domain_name_root}0", response)
        self.assertNotIn(f"{TestData.test_domain_name_root}1", response)
        self.assertNotIn(f"{TestData.test_domain_name_root}2", response)
        self.assertIn(TestData.test_domain_name_root, response)


if __name__ == '__main__':
    unittest.main()
