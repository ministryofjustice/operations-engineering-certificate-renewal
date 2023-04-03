import requests
from notifications_python_client.notifications import NotificationsAPIClient


class NotifyService:
    def __init__(self, config, api_key):
        self.config = config
        self.api_key = api_key

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

    def _send_email(self, email_params):
        for email in email_params['email_addresses']:
            try:
                NotificationsAPIClient(self.api_key).send_email_notification(
                    email_address=email,
                    template_id=self.config['template_ids']['cert_expiry'],
                    personalisation=email_params
                )
            except requests.exceptions.HTTPError as api_key_error:
                raise requests.exceptions.HTTPError(
                    f"You may need to export your Notify API Key:\n {api_key_error}"
                ) from api_key_error

    def send_emails_from_parameters(self, email_parameter_list):
        for email_parameters in email_parameter_list:
            self._send_email(email_parameters)

    def send_test_email_from_parameters(self, email_parameter_list, test_email):
        print(f"Sending test email: {email_parameter_list} and email: {test_email}")
        for email_parameters in email_parameter_list:
            print(f"Running through each email... {email_parameters} in {email_parameter_list}")
            try:
                NotificationsAPIClient(self.api_key).send_email_notification(
                    email_address=test_email,
                    template_id=self.config['template_ids']['cert_expiry'],
                    personalisation=email_parameters
                )
            except requests.exceptions.HTTPError as api_key_error:
                raise requests.exceptions.HTTPError(
                    f"You may need to export your Notify API Key:\n {api_key_error}"
                ) from api_key_error
