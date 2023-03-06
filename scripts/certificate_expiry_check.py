import sys
import os
import datetime
import json
import requests
import argparse
from notifications_python_client.notifications import NotificationsAPIClient


# Most of these will need to be env vars/secrets

reply_email = "certificates@digital.justice.gov.uk"
gandi_url = "https://api.gandi.net/"
certificate_email_template_id = "06abd028-0a8f-43d9-a122-90a92f9b62ee"
gandi_api_key = ""
notify_api_key = ""

warn_1 = 30
warn_2 = 15
warn_3 = 1


def main():
    global gandi_api_key
    global notify_api_key

    with open('./resources/mappings.json') as file:
        mappings = file.read()

    the_big_list = json.loads(mappings)

    # This will change when moving to a GitHub action
    try:
        gandi_api_key = os.environ.get('GANDI_API_KEY')
        notify_api_key = os.environ.get('NOTIFY_API_KEY')
    except (TypeError) as e:
        raise TypeError("Please ensure you've exported your API keys.")

    find_expiring_certificates(the_big_list)


def find_expiring_certificates(the_big_list):
    '''
    Finds all certificates that are due to expire, and send emails if they meet the criteria.
    '''

    url_extension = '/v5/certificate/issued-certs'
    HEADERS = {'Authorization': 'ApiKey ' + gandi_api_key}

    # per_page is essentially a limit on the returned values, so this is set to 1000 to ensure all results are returned.
    PARAMS = {'per_page': 1000}

    try:
        r = requests.get(url=gandi_url+url_extension,
                         params=PARAMS, headers=HEADERS)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise SystemExit(f"You may need to export your Gandi API Key!\n {e}")

    data = r.json()

    for item in data:
        if item['status'] == 'valid' and the_big_list[item['cn']]['owner'] == 'OE':
            date = datetime.datetime.strptime(
                item['dates']['ends_at'], '%Y-%m-%dT%H:%M:%SZ').date()
            if date == (datetime.datetime.today() + datetime.timedelta(days=warn_1)).date():
                send_email('expire', build_params(
                    item['cn'], warn_1), the_big_list)
            elif date == (datetime.datetime.today() + datetime.timedelta(days=warn_2)).date():
                send_email('expire', build_params(
                    item['cn'], warn_2), the_big_list)
            elif date == (datetime.datetime.today() + datetime.timedelta(days=warn_3)).date():
                send_email('expire', build_params(
                    item['cn'], warn_3), the_big_list)


def build_params(domain_name: str, days: int, the_big_list):
    emails = retrieve_email_list(domain_name, the_big_list)
    params = {
        'email_addresses': emails,
        'domain_name': domain_name,
        'csr_email': reply_email,
        'end_date': 'date',
        'days': days
    }

    return params


def retrieve_email_list(domain: str, the_big_list):
    if domain in the_big_list and the_big_list[domain]["owner"] == "OE":
        print(f"The domain exists and is owned by Operations Engineering.")
        email_list = [the_big_list[domain]["recipient"]]
        for email in the_big_list[domain]["recipientcc"]:
            email_list.append(email)
        return email_list
    return False


def send_email(type, params):
    notifications_client = NotificationsAPIClient(notify_api_key)

    if type == 'expire':
        try:
            response = notifications_client.send_email_notification(
                email_address='sam.pepper@digital.justice.gov.uk',
                template_id=certificate_email_template_id,
                personalisation=params
            )
        except requests.exceptions.HTTPError as e:
            raise SystemExit(
                f"You may need to export your Notify API Key!\n {e}")

        print('EMAIL SENT!')
    return response

# def get_certificate_information(cert):
#     '''
#     For returning a particular certificate based on it's domain name.
#     '''

#     URL = 'https://api.gandi.net/v5/certificate/issued-certs'
#     PARAMS = {'cn': cert}
#     HEADERS = {'Authorization': 'ApiKey ' + gandi_api_key}

#     try:
#         r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
#         data = r.json()
#         id = data[0]['id']
#     except:
#         print("Could not reach Gandi.")


if __name__ == "__main__":
    main()
