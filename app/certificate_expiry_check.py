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


def find_expiring_certificates(email_list, certificate_list):
    """
    Finds all certificates that are due to expire, and sends an email if they meet the criteria.
    """





def build_params(domain_name: str, email_list, date, reply_email: str):
    emails = retrieve_email_list(domain_name, email_list)
    params = {
        'email_addresses': emails,
        'domain_name': domain_name,
        'csr_email': reply_email,
        'end_date': str(date)
    }
    return params


def retrieve_email_list(domain: str, email_list):
    filtered_email_list = []
    if email_list[domain]['external_cname']:
        for email in email_list[domain]['external_cname']:
            filtered_email_list.append(email)
        filtered_email_list.append(config['reply_email'])
        return filtered_email_list
    print(f"The domain exists and is owned by Operations Engineering.")
    filtered_email_list.append(email_list[domain]["recipient"])
    for email in email_list[domain]["recipientcc"]:
        filtered_email_list.append(email)
    filtered_email_list.append(config['reply_email'])
    return filtered_email_list


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
    gandi_service = GandiService()

    # Get a list of the email mappings from S3
    email_mappings = s3_service.get_json_file(config['s3']['s3_bucket_name'], config['s3']['s3_object_name'],
                                              './app/s3_email_mapping.json')

    # Get a list of the expired certificates from Gandi
    certificate_list = gandi_service.get_expiring_certificates(config)

    # Send emails for the expired certificates using Notify

    # Send report email to OE

    find_expiring_certificates(email_mappings, certificate_list)


if __name__ == "__main__":
    main()
