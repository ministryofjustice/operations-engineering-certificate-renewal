import unittest
from unittest.mock import patch
from scripts import certificate_expiry_check


class TestCertificateExpiry(unittest.TestCase):
    def test_matching_domain_returns_correct_data(self):
        test_data = {
            "test_list": {
                "matching.domain.gov.uk": {
                    "recipient": "test.user@mail.com",
                    "recipientcc": [],
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

        self.assertIn(test_data['test_list']
                         [test_data['test_domain']]['recipient'], result)

    def test_non_matching_domain_returns_false(self):
        test_data = {
            "test_list": {
                "matching.domain.gov.uk": {
                    "recipient": "test.user@mail.com",
                    "recipientcc": [],
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

    def test_external_cname_returned_when_present(self):
        test_data = {
            "test_list": {
                "matching.domain.gov.uk": {
                    "recipient": "test.user@mail.com",
                    "recipientcc": [],
                    "owner": "OE",
                    "external_cname": ["external.person@mail.com"]
                }
            },
            "test_domain": "matching.domain.gov.uk"
        }

        result = certificate_expiry_check.retrieve_email_list(
            test_data['test_domain'],
            test_data['test_list']
        )

        self.assertIn(test_data['test_list']
                         [test_data['test_domain']]['external_cname'][0], result)

    def test_matching_domain_returns_multiple_emails(self):
        test_data = {
            "test_list": {
                "matching.domain.gov.uk": {
                    "recipient": "test.user@mail.com",
                    "recipientcc": [
                        "another.user@mail.com",
                        "yet.another.user@mail.com"
                    ],
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

        self.assertIn(test_data['test_list']
                         [test_data['test_domain']]['recipient'], result)
        self.assertIn(test_data['test_list']
                         [test_data['test_domain']]['recipientcc'][0], result)
        self.assertIn(test_data['test_list']
                         [test_data['test_domain']]['recipientcc'][1], result)


if __name__ == '__main__':
    unittest.main()
