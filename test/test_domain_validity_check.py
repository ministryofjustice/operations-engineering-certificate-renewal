import unittest
from unittest.mock import patch
from scripts import certificate_expiry_check


class TestDomainValidityCheck(unittest.TestCase):

    def test_domain_validity_check_returns_false_with_non_matching_domain(self):
        test_data = {
            "test_item": {
                "cn": "matching.domain.gov.uk",
                "status": "valid"

            },
            "test_list": {
                "non.matching.domain.gov.uk": {
                    "owner": "OE"
                }
            }
        }

        result = certificate_expiry_check.domain_validity_check(
            test_data['test_item'], test_data['test_list'])

        self.assertFalse(result)

    def test_domain_validity_check_returns_false_incorrect_owner(self):
        test_data = {
            "test_item": {
                "cn": "matching.domain.gov.uk",
                "status": "valid"

            },
            "test_list": {
                "matching.domain.gov.uk": {
                    "owner": "HMCTS"
                }
            }
        }

        result = certificate_expiry_check.domain_validity_check(
            test_data['test_item'], test_data['test_list'])

        self.assertFalse(result)

    def test_domain_validity_check_returns_false_with_invalid_state(self):
        test_data = {
            "test_item": {
                "cn": "matching.domain.gov.uk",
                "status": "pending"

            },
            "test_list": {
                "matching.domain.gov.uk": {
                    "owner": "OE"
                }
            }
        }

        result = certificate_expiry_check.domain_validity_check(
            test_data['test_item'], test_data['test_list'])

        self.assertFalse(result)

    def test_domain_validity_check_returns_true_with_correct_information(self):
        test_data = {
            "test_item": {
                "cn": "matching.domain.gov.uk",
                "status": "valid"

            },
            "test_list": {
                "matching.domain.gov.uk": {
                    "owner": "OE"
                }
            }
        }

        result = certificate_expiry_check.domain_validity_check(
            test_data['test_item'], test_data['test_list'])

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
