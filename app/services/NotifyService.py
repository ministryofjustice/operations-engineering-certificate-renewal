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

    def _send_report_email(self, report_string):
        try:
            NotificationsAPIClient(self.api_key).send_email_notification(
                email_address='sam.pepper@digital.justice.gov.uk',
                template_id=self.config['template_ids']['report'],
                personalisation={
                    "report": report_string
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

    def _build_report_string(self, email_parameter_list):
        return "".join(
            f"{email_parameter['domain_name']} went to {email_parameter['email_addresses']}, expiring on: {email_parameter['end_date']} \n"
            for email_parameter in email_parameter_list
        )

    def send_emails_from_parameters(self, email_parameter_list):
        for email_parameters in email_parameter_list:
            self._send_email(email_parameters,
                             email_parameters['email_addresses'])

    def send_report_email_to_operations_engineering(self, email_parameter_list):
        self._send_report_email(
            self._build_report_string(email_parameter_list))

    def send_test_email_from_parameters(self, email_parameter_list, test_email):
        for email_parameters in email_parameter_list:
            self._send_email(email_parameters, [test_email])
