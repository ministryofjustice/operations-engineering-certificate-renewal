import os
import unittest
from unittest.mock import patch

from app import certificate_expiry_check


class TestBuildParameters(unittest.TestCase):

    @patch('app.certificate_expiry_check.retrieve_email_list')
    def test_build_parameters_returns_expected_data(self, mock_retrieve_email_list):
        test_data = {
            "domain": "www.test.com",
            "date": "2022-03-03",
            "reply_email": "reply@digital.gov.uk",
            "test_list": {'test': 'test'},
            "test_email_addresses": ['test@digital.justice.gov.uk']
        }

        mock_retrieve_email_list.return_value = test_data['test_email_addresses']

        result = certificate_expiry_check.build_params(
            test_data['domain'], test_data['test_list'], test_data['date'], test_data['reply_email']
        )

        self.assertEqual(result['domain_name'], test_data['domain'])
        self.assertEqual(result['email_addresses'],
                         test_data['test_email_addresses'])


if __name__ == '__main__':
    unittest.main()
