import sys
import os
import requests
import argparse
from notifications_python_client.notifications import NotificationsAPIClient


def get_certificate_information(cert):
    # Fetch the api key for Gandi from the environment
    try:
        api_key = os.environ.get('GANDI_API_KEY')
        notify_api_key = os.environ.get('NOTIFY_API_KEY')
    except (TypeError):
        sys.exit('Please export your Gandi API Key!')

    notifications_client = NotificationsAPIClient(notify_api_key)

    response = notifications_client.send_email_notification(
        email_address='sam.pepper@digital.justice.gov.uk',
        template_id='72cd9e80-cf0c-4504-bee8-3b1acc3f0f9b',
        personalisation={
            'first_name': 'Sam',
            'test_var': 'something',
        }
    )

    print(f'This was the response: {response}')

    URL = 'https://api.gandi.net/v5/certificate/issued-certs'
    PARAMS = {'cn': cert}
    HEADERS = {'Authorization': 'ApiKey ' + api_key}

    try:
        r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
        data = r.json()
        id = data[0]['id']

        # print(f"Information returned: {data}")
        print(f'ID: {id}')
    except:
        print("Could not reach Gandi.")


print(f"Starting script...")
# Creates and parses certain arguments for the script to run.
parser = argparse.ArgumentParser(
    description="Fetch information on a particular domain's certificate.")
parser.add_argument(
    "-c", "--cert", help="The name of the domain you'd like to view the information of.", required=True)
argument = parser.parse_args()

get_certificate_information(argument.cert)
print(f"Stopping script...")
sys.exit()
