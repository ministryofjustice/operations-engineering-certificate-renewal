from notifications_python_client import NotificationsAPIClient


class NotifyService:
    def __init__(self, config):
        self.config = config
        self.client = NotificationsAPIClient(
            config['keys']['notify_api_key'])

    def send_email(self):
        print('Sending email...')
