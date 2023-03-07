import requests
import os
from notifications_python_client.notifications import NotificationsAPIClient


def send_email():
    notifications_client = NotificationsAPIClient(os.environ['NOTIFY_API_KEY'])

    try:
        response = notifications_client.send_email_notification(
            email_address='sam.pepper@digital.justice.gov.uk',
            template_id="72cd9e80-cf0c-4504-bee8-3b1acc3f0f9b",
            personalisation={
                "first_name": "Sam",
                "test_var": "test"
            }
        )

        print(f"Response: {response}")
    except requests.exceptions.HTTPError as e:
        raise SystemExit(
            f"You may need to export your Notify API Key!\n {e}")

    print('EMAIL SENT!')


send_email()
