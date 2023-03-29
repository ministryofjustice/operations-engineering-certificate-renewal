import datetime

import requests


class GandiService:
    def __init__(self, config, api_key, base_url, url_extension) -> None:
        self.config = config
        self.headers = {'Authorization': f'ApiKey {api_key}'}
        self.params = {'per_page': 1000}
        self.url = base_url + url_extension

    def _get_email_address_of_domain_owners(self, domain_name, email_list):
        if email_list[domain_name]['external_cname']:
            return email_list[domain_name]['external_cname']
        email_addresses_of_domain_owners = [
            email_list[domain_name]['recipient']]
        if email_list[domain_name]['recipientcc']:
            email_addresses_of_domain_owners.extend(
                iter(email_list[domain_name]['recipientcc'])
            )
        return email_addresses_of_domain_owners

    def _check_certificate_state(self, domain_item, email_list, certificate_state) -> bool:
        return domain_item['cn'] in email_list and domain_item['status'] == certificate_state

    def _is_certificate_owned_by_operations_engineering(self, domain_item, email_list):
        return email_list[domain_item['cn']]['owner'] == 'OE'

    def _get_days_between_now_and_expiry_date(self, expiry_date):
        return (expiry_date - datetime.datetime.now()).days

    def _format_expiry_date(self, date_string: str) -> datetime.date:
        return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ').date()

    def get_certificate_list(self):
        try:
            response = requests.get(
                url=self.url, params=self.params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as authentication_error:
            raise requests.exceptions.HTTPError(
                f"You may need to export your Gandi API key:\n {authentication_error}") from authentication_error
        except TypeError as api_key_error:
            raise TypeError(
                f"Gandi API key does not exist or is in the wrong format:\n {api_key_error}") from api_key_error

    def get_certificates_in_valid_state(self, certificate_list, email_list):
        valid_state_certificates = {}
        for domain_item in certificate_list:
            if self._check_certificate_state(domain_item, email_list, 'valid') and \
                    self._is_certificate_owned_by_operations_engineering(domain_item, email_list):
                expiry_date = self._format_expiry_date(
                    domain_item['dates']['ends_at'])
                valid_state_certificates[domain_item['cn']] = {
                    "expiry_date": expiry_date
                }
        return valid_state_certificates

    def get_expired_certificates_from_valid_certificate_list(self, valid_state_certificate_list: dict, email_list):
        expired_certificates = {}
        for domain_item in valid_state_certificate_list:
            days_between_now_and_expiry_date = self._get_days_between_now_and_expiry_date(
                valid_state_certificate_list[domain_item]['expiry_date'])
            if days_between_now_and_expiry_date in self.config['cert_expiry_thresholds']:
                email_addresses_of_domain_owners = \
                    self._get_email_address_of_domain_owners(
                        domain_item, email_list)
                expired_certificates[domain_item] = {
                    "days": days_between_now_and_expiry_date,
                    "emails": email_addresses_of_domain_owners
                }
        return expired_certificates
