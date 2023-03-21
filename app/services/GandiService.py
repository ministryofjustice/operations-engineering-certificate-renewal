import datetime

import requests


class GandiService:
    def __init__(self, config, api_key, base_url, url_extension) -> None:
        self.config = config
        self.headers = {'Authorization': 'ApiKey ' + api_key}
        self.params = {'per_page': 1000}
        self.url = base_url + url_extension

    def get_expiring_certificates(self, email_list):
        expired_certificates = {}
        try:
            certificate_list = requests.get(
                url=self.url,
                params=self.params,
                headers=self.headers)
            certificate_list.raise_for_status()
        except requests.exceptions.HTTPError as authentication_error:
            raise requests.exceptions.HTTPError(
                f"You may need to export your Gandi API key:\n {authentication_error}")
        except TypeError as api_key_error:
            raise TypeError(
                f"Gandi API key does not exist or is in the wrong format:\n {api_key_error}")

        for domain_item in certificate_list.json():
            if domain_item['cn'] in email_list and domain_item['status'] == 'valid':
                if email_list[domain_item['cn']]['owner'] == 'OE':
                    date = datetime.datetime.strptime(
                        domain_item['dates']['ends_at'], '%Y-%m-%dT%H:%M:%SZ').date()
                    for threshold in self.config['cert_expiry_thresholds']:
                        if date == (datetime.datetime.today() + datetime.timedelta(days=threshold)).date():
                            emails = []
                            if email_list[domain_item['cn']]['external_cname']:
                                for e in email_list[domain_item['cn']]['external_cname']:
                                    emails.append(e)
                            else:
                                emails = [
                                    email_list[domain_item['cn']]['recipient']]
                                if email_list[domain_item['cn']]['recipientcc']:
                                    for e in email_list[domain_item['cn']]['recipientcc']:
                                        emails.append(e)
                            expired_certificates[domain_item['cn']] = {
                                "days": threshold,
                                "emails": emails
                            }
        return expired_certificates
