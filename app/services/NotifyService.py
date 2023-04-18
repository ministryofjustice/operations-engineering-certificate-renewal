from datetime import datetime, timezone

import requests
from notifications_python_client.notifications import NotificationsAPIClient


class NotifyService:
    def __init__(self, config, api_key):
        self.config = config
        self.api_key = api_key

    def _get_notifications_by_type_and_status(self, template_type, status):
        return NotificationsAPIClient(self.api_key).get_all_notifications(status=status, template_type=template_type)

    def send_report_email(self, report, template_id, email):
        try:
            NotificationsAPIClient(self.api_key).send_email_notification(
                email_address=email,
                template_id=template_id,
                personalisation={
                    "report": report
                }
            )
        except requests.exceptions.HTTPError as api_key_error:
            raise requests.exceptions.HTTPError(
                f"You may need to export your Notify API Key:\n {api_key_error}"
            ) from api_key_error

    def _send_email(self, email_params, recipients):
        for email in recipients:
            try:
                NotificationsAPIClient(self.api_key).send_email_notification(
                    email_address=email,
                    template_id=self.config['template_ids']['cert_expiry'],
                    personalisation={
                        "domain_name": email_params['domain_name'],
                        "csr_email": email_params['csr_email'],
                        "end_date": email_params['end_date'].strftime('%d/%m/%Y')
                    }
                )
            except requests.exceptions.HTTPError as api_key_error:
                raise requests.exceptions.HTTPError(
                    f"You may need to export your Notify API Key:\n {api_key_error}"
                ) from api_key_error

    def build_email_parameter_list(self, valid_certificate_list):
        emails_parameter_list = []
        for valid_certificate in valid_certificate_list:
            params = {
                'email_addresses': valid_certificate_list.get(valid_certificate).get('emails'),
                'domain_name': valid_certificate,
                'csr_email': self.config['reply_email'],
                'end_date': valid_certificate_list.get(valid_certificate).get('expiry_date')
            }
            emails_parameter_list.append(params)
        return emails_parameter_list

    def build_main_report_string(self, email_parameter_list):
        new_line = '\n'
        return "".join(
            f"Domain Name: {email_parameter['domain_name']}\n"
            f"Sent to:\n{''.join([f'{address}{new_line}' for address in email_parameter['email_addresses']])}"
            f"\nExpiry Date: {email_parameter['end_date']} \n\n"
            for email_parameter in email_parameter_list
        )

    def build_undeliverable_email_report_string(self, undeliverable_email_list):
        if undeliverable_email_list is None:
            return

        return "".join(
            f"Email Address: {undeliverable_email['email_address']}\n"
            f"Sent at: {undeliverable_email['created_at']}\n"
            f"Status: {undeliverable_email['status']} \n\n"
            for undeliverable_email in undeliverable_email_list
        )

    def send_emails_from_parameters(self, email_parameter_list):
        for email_parameters in email_parameter_list:
            self._send_email(email_parameters,
                             email_parameters['email_addresses'])

    def send_test_email_from_parameters(self, email_parameter_list, test_email):
        for email_parameters in email_parameter_list:
            self._send_email(email_parameters, [test_email])

    def check_for_undelivered_emails_for_template(self, template_id):
        notifications = self._get_notifications_by_type_and_status('email', 'failed')[
            'notifications']
        today = datetime.now(timezone.utc).date()

        undelivered_emails = []

        for notification in notifications:
            created_at = datetime.fromisoformat(
                notification['created_at']).date()

            if notification['template']['id'] == template_id and created_at == today:
                undelivered_email = {
                    "email_address": notification['email_address'],
                    "created_at": created_at,
                    "status": notification['status']
                }
                undelivered_emails.append(undelivered_email)
        return undelivered_emails
