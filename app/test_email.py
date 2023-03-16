import os
import requests
from notifications_python_client.notifications import NotificationsAPIClient
from pyaml_env import parse_config

config_location = os.getenv(
    "CONFIG_CONTEXT", default="../configs/production.yml")
config = parse_config(config_location)


def send_email():
    notifications_client = NotificationsAPIClient(
        config['keys']['notify_api_key'])
    try:
        response = notifications_client.send_email_notification(
            email_address=
            'sam.pepper@digital.justice.gov.uk, connor.glynn@digital.justice.gov.uk, '
            'nick.walters@digital.justice.gov.uk',
            template_id='72cd9e80-cf0c-4504-bee8-3b1acc3f0f9b',
            personalisation={
                "first_name": "Name",
                "test_var": "Test"
            }
        )
    except requests.exceptions.HTTPError as api_key_error:
        raise SystemExit(
            f"You may need to export your Notify API Key:\n {api_key_error}")
    return response


if __name__ == "__main__":
    send_email()
