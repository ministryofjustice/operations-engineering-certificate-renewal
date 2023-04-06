import unittest
from unittest.mock import patch

import requests

from app.services.NotifyService import NotifyService
from test.resources.test_data import TestData
from test.test_config import test_config


class TestBuildParameters(unittest.TestCase):
    def setUp(self):
        self.config = test_config
        self.api_key = 'test_api_key'
        self.notify_service = NotifyService(self.config, self.api_key)

    def test_build_parameters_returns_multiple_expected_domains(self):
        test_case_count = 3
        data = TestData.generate_multiple_valid_certificate_list(
            count=test_case_count)
        response = self.notify_service.build_email_parameter_list(data)

        self.assertIn(f"{TestData.test_domain_name_root}{0}",
                      response[0]['domain_name'])
        self.assertIn(f"{TestData.test_domain_name_root}{1}",
                      response[1]['domain_name'])
        self.assertIn(f"{TestData.test_domain_name_root}{2}",
                      response[2]['domain_name'])

    def test_build_parameters_returns_multiple_expected_domains_with_expected_email(self):
        test_case_count = 3
        data = TestData.generate_multiple_valid_certificate_list(
            count=test_case_count)
        response = self.notify_service.build_email_parameter_list(data)

        self.assertIn(f"{TestData.test_recipient_email_root}{0}",
                      response[0]['email_addresses'])
        self.assertIn(f"{TestData.test_recipient_email_root}{1}",
                      response[1]['email_addresses'])
        self.assertIn(f"{TestData.test_recipient_email_root}{2}",
                      response[2]['email_addresses'])

    def test_build_parameters_returns_multiple_expected_emails(self):
        test_case_count = 3
        data = TestData.generate_single_valid_certificate_multiple_emails(
            count=test_case_count)
        response = self.notify_service.build_email_parameter_list(data)

        self.assertIn(f"{TestData.test_recipient_email_root}",
                      response[0]['email_addresses'][0])
        self.assertIn(f"{TestData.test_recipient_email_root}",
                      response[0]['email_addresses'][1])
        self.assertIn(f"{TestData.test_recipient_email_root}",
                      response[0]['email_addresses'][2])


@patch.object(NotifyService, '_send_email')
class TestSendEmail(unittest.TestCase):

    def setUp(self):
        self.config = test_config
        self.api_key = 'test_api_key'
        self.notify_service = NotifyService(self.config, self.api_key)

    def test_send_emails_from_parameters_sends_emails(self, mock_send_email):
        email_parameter_list = TestData.generate_multiple_email_parameter_list(
            count=3)

        self.notify_service.send_emails_from_parameters(email_parameter_list)
        mock_send_email.assert_any_call(
            email_parameter_list[0], email_parameter_list[0]['email_addresses'])
        mock_send_email.assert_any_call(
            email_parameter_list[1], email_parameter_list[1]['email_addresses'])
        mock_send_email.assert_any_call(
            email_parameter_list[2], email_parameter_list[2]['email_addresses'])

    def test_email_does_not_send_with_empty_list(self, mock_send_email):
        email_parameter_list = []
        self.notify_service.send_emails_from_parameters(email_parameter_list)
        mock_send_email.assert_not_called()

    def test_send_emails_from_parameters_handles_http_error(self, mock_send_email):
        mock_send_email.side_effect = requests.exceptions.HTTPError(
            'API Key error')
        email_parameter_list = TestData.generate_multiple_email_parameter_list()
        with self.assertRaises(requests.exceptions.HTTPError) as context:
            self.notify_service.send_emails_from_parameters(
                email_parameter_list)

        expected_message = "API Key error"
        self.assertEqual(str(context.exception), expected_message)


class TestSendReportEmail(unittest.TestCase):

    def setUp(self):
        self.config = test_config
        self.api_key = 'test_api_key'
        self.template_id = 'test_template_id'
        self.ops_email = 'test_ops_email'
        self.notify_service = NotifyService(self.config, self.api_key)

    @patch("app.services.NotifyService.NotificationsAPIClient")
    def test_send_main_report_is_sent_with_expected_data(self, mock_notifications_api_client):
        test_main_report_data = TestData.generate_main_report_single_domain_single_email()

        mock_notifications_api_client.return_value.send_email_notification.return_value = None
        self.notify_service.send_report_email(test_main_report_data, self.template_id, self.ops_email)

        mock_notifications_api_client.return_value.send_email_notification.assert_called_once_with(
            email_address=self.ops_email,
            template_id=self.template_id,
            personalisation={
                "report": test_main_report_data
            }
        )

    @patch("app.services.NotifyService.NotificationsAPIClient")
    def test_send_main_report_with_multiple_domains_is_sent_with_expected_data(self, mock_notifications_api_client):
        test_case_count = 3
        test_main_report_data = TestData.generate_main_report_multiple_domain_multiple_email(
            test_case_count, test_case_count)

        mock_notifications_api_client.return_value.send_email_notification.return_value = None
        self.notify_service.send_report_email(test_main_report_data, self.template_id, self.ops_email)

        mock_notifications_api_client.return_value.send_email_notification.assert_called_once_with(
            email_address=self.ops_email,
            template_id=self.template_id,
            personalisation={
                "report": test_main_report_data
            }
        )

    @patch("app.services.NotifyService.NotificationsAPIClient")
    def test_send_undeliverable_report_is_sent_with_expected_data(self, mock_notifications_api_client):
        test_undeliverable_report_data = TestData.generate_undeliverable_report_single_email()

        mock_notifications_api_client.return_value.send_email_notification.return_value = None
        self.notify_service.send_report_email(test_undeliverable_report_data, self.template_id, self.ops_email)

        mock_notifications_api_client.return_value.send_email_notification.assert_called_once_with(
            email_address=self.ops_email,
            template_id=self.template_id,
            personalisation={
                "report": test_undeliverable_report_data
            }
        )

    @patch("app.services.NotifyService.NotificationsAPIClient")
    def test_send_undeliverable_report_with_multiple_domains_is_sent_with_expected_data(
            self, mock_notifications_api_client):
        test_case_count = 3
        test_undeliverable_report_data = TestData.generate_undeliverable_report_multiple_email(test_case_count)

        mock_notifications_api_client.return_value.send_email_notification.return_value = None
        self.notify_service.send_report_email(test_undeliverable_report_data, self.template_id, self.ops_email)

        mock_notifications_api_client.return_value.send_email_notification.assert_called_once_with(
            email_address=self.ops_email,
            template_id=self.template_id,
            personalisation={
                "report": test_undeliverable_report_data
            }
        )
