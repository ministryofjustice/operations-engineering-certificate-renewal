import unittest
from unittest.mock import patch
from scripts import certificate_expiry_check


class TestCertificateExpiry(unittest.TestCase):

    @patch('scripts.certificate_expiry_check.retrieve_email_list')
    def test_build_parameters_returns_expected_data(self, mock_retrieve_email_list):

        test_data = {
            "domain": "www.test.com",
            "days": 24,
            "test_list": {'test': 'test'},
            "test_email_addresses": ['test@digital.justice.gov.uk']
        }

        mock_retrieve_email_list.return_value = test_data['test_email_addresses']

        result = certificate_expiry_check.build_params(
            test_data['domain'], test_data['days'], test_data['test_list']
        )

        self.assertEqual(result['domain_name'], test_data['domain'])
        self.assertEqual(result['days'], test_data['days'])
        self.assertEqual(result['email_addresses'],
                         test_data['test_email_addresses'])

    def test_matching_domain_returns_correct_data(self):
        test_data = {
            "test_list": {
                "matching.domain.gov.uk": {
                    "recipient": "test_user@mail.com",
                    "recipientcc": "",
                    "owner": "OE",
                    "external_cname": []
                }
            },
            "test_domain": "matching.domain.gov.uk"
        }

        result = certificate_expiry_check.retrieve_email_list(
            test_data['test_domain'],
            test_data['test_list']
        )

        self.assertEqual(result[0], test_data['test_list']
                         [test_data['test_domain']]['recipient'])

    def test_non_matching_domain_returns_false(self):
        test_data = {
            "test_list": {
                "matching.domain.gov.uk": {
                    "recipient": "test_user@mail.com",
                    "recipientcc": "",
                    "owner": "OE",
                    "external_cname": []
                }
            },
            "test_domain": "non.matching.domain.gov.uk"
        }

        result = certificate_expiry_check.retrieve_email_list(
            test_data['test_domain'],
            test_data['test_list']
        )

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
