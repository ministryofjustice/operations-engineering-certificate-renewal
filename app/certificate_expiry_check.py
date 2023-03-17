import datetime
import json
import os

import boto3
import requests
from notifications_python_client.notifications import NotificationsAPIClient
from pyaml_env import parse_config

config_location = os.getenv(
    "CONFIG_CONTEXT", default="../configs/production.yml")
config = parse_config(config_location)


def find_expiring_certificates(email_list):
    """
    Finds all certificates that are due to expire, and sends an email if they meet the criteria.
    """
    headers = {'Authorization': 'ApiKey ' + config['keys']['gandi_api_key']}
    params = {'per_page': 1000}

    try:
        certificate_list = requests.get(
            url=config['urls']['gandi_base_url'] +
            config['urls']['gandi_cert_url_extension'],
            params=params, headers=headers)
        certificate_list.raise_for_status()
    except requests.exceptions.HTTPError as authentication_error:
        raise SystemExit(
            f"You may need to export your Gandi API key:\n {authentication_error}")
    except TypeError as api_key_error:
        raise TypeError(
            f"Gandi API key does not exist or is in the wrong format:\n {api_key_error}")

    domain_list = certificate_list.json()

    for domain_item in domain_list:
        if domain_validity_check(domain_item, email_list):
            date = datetime.datetime.strptime(
                domain_item['dates']['ends_at'], '%Y-%m-%dT%H:%M:%SZ').date()
            for threshold in config['cert_expiry_thresholds']:
                if date == (datetime.datetime.today() + datetime.timedelta(days=threshold)).date():
                    send_email('expire', build_params(
                        domain_item['cn'], email_list, date, config['reply_email']))
                    break


def domain_validity_check(item, email_list):
    domain_exists_in_map = item['cn'] in email_list
    domain_is_in_valid_state = item['status'] == 'valid'
    if domain_exists_in_map and domain_is_in_valid_state:
        domain_is_owned_by_ops_eng = email_list[item['cn']]["owner"] == "OE"
        return domain_is_owned_by_ops_eng
    return False


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

    temporary_emails = ['sam.pepper@digital.justice.gov.uk']

    if email_type == 'expire':
        for email in temporary_emails:
            try:
                notifications_client.send_email_notification(
                    email_address=email,
                    template_id=config['template_ids']['cert_expiry'],
                    personalisation=params
                )
            except requests.exceptions.HTTPError as api_key_error:
                raise SystemExit(
                    f"You may need to export your Notify API Key:\n {api_key_error}")


if __name__ == "__main__":

    file_path = './app/s3_email_mapping.json'
    s3 = boto3.client('s3')

    with open(file_path, 'wb') as file:
        s3.download_fileobj(
            config['s3']['s3_bucket_name'], config['s3']['s3_object_name'], file)
    with open(file_path) as file:
        mappings = file.read()

    email_map = json.loads(mappings)
    find_expiring_certificates(email_map)
