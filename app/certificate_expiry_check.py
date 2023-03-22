import datetime
import os

import requests
from notifications_python_client.notifications import NotificationsAPIClient
from pyaml_env import parse_config

from app.services.S3Service import S3Service
from app.services.GandiService import GandiService

config_location = os.getenv(
    "CONFIG_CONTEXT", default="../configs/production.yml")
config = parse_config(config_location)


def build_params(domain_name: str, email_list, date, reply_email: str):
    emails = retrieve_email_list(domain_name, email_list)
    params = {
        'email_addresses': emails,
        'domain_name': domain_name,
        'csr_email': reply_email,
        'end_date': str(date)
    }
    return params


def send_email(email_type, params):
    notifications_client = NotificationsAPIClient(
        config['keys']['notify_api_key'])

    if email_type == 'expire':
        for email in params['email_addresses']:
            try:
                notifications_client.send_email_notification(
                    email_address=email,
                    template_id=config['template_ids']['cert_expiry'],
                    personalisation=params
                )
            except requests.exceptions.HTTPError as api_key_error:
                raise SystemExit(
                    f"You may need to export your Notify API Key:\n {api_key_error}")


def main():
    # Instantiate services
    s3_service = S3Service()
    gandi_service = GandiService(config,
                                 config['keys']['gandi_api_key'],
                                 config['urls']['gandi_base_url'],
                                 config['urls']['gandi_cert_url_extension'])

    # Get a list of the email mappings from S3
    email_mappings = s3_service.get_json_file(config['s3']['s3_bucket_name'], config['s3']['s3_object_name'],
                                              './app/s3_email_mapping.json')

    # Get a list of the expired certificates from Gandi
    certificate_list = gandi_service.get_certificate_list()
    expired_certificates = gandi_service.get_expired_certificates(
        certificate_list, email_mappings)

    # Send emails for the expired certificates using Notify
    # TODO

    # Send report email to OE
    # TODO


if __name__ == "__main__":
    main()
