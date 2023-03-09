import datetime
import requests
from notifications_python_client.notifications import NotificationsAPIClient
import config


def find_expiring_certificates(email_list):
    """
    Finds all certificates that are due to expire, and sends an email if they meet the criteria.
    """

    headers = {'Authorization': 'ApiKey ' + config.GANDI_API_KEY}
    params = {'per_page': 1000}

    try:
        certificate_list = requests.get(url=config.GANDI_BASE_URL + config.CERT_URL_EXTENSION,
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
            for threshold in config.CERT_EXPIRY_THRESHOLDS:
                if date == (datetime.datetime.today() + datetime.timedelta(days=threshold)).date():
                    send_email('expire', build_params(
                        domain_item['cn'], threshold, email_list, date))
                    break


def domain_validity_check(item, email_list):
    domain_exists_in_map = item['cn'] in email_list
    domain_is_in_valid_state = item['status'] == 'valid'
    if domain_exists_in_map and domain_is_in_valid_state:
        domain_is_owned_by_ops_eng = email_list[item['cn']]["owner"] == "OE"
        return domain_is_owned_by_ops_eng
    return False


def build_params(domain_name: str, days: int, email_list, date):
    emails = retrieve_email_list(domain_name, email_list)
    params = {
        'email_addresses': emails,
        'domain_name': domain_name,
        'csr_email': config.DEFAULT_REPLY_EMAIL,
        'end_date': str(date),
        'days': days
    }

    return params


def retrieve_email_list(domain: str, email_list):
    filtered_email_list = []
    domain_contains_external_cname = email_list[domain]['external_cname'] is not None
    if domain_contains_external_cname:
        for email in email_list[domain]['external_cname']:
            filtered_email_list.append(email)
            return filtered_email_list
    print(f"The domain exists and is owned by Operations Engineering.")
    filtered_email_list.append(email_list[domain]["recipient"])
    for email in email_list[domain]["recipientcc"]:
        filtered_email_list.append(email)
    return filtered_email_list


def send_email(email_type, params):

    notifications_client = NotificationsAPIClient(config.NOTIFY_API_KEY)

    if email_type == 'expire':
        try:
            response = notifications_client.send_email_notification(
                email_address='sam.pepper@digital.justice.gov.uk',
                template_id=config.CERT_EXPIRE_EMAIL_TEMPLATE_ID,
                personalisation=params
            )
        except requests.exceptions.HTTPError as api_key_error:
            raise SystemExit(
                f"You may need to export your Notify API Key:\n {api_key_error}")
        return response


if __name__ == "__main__":
    find_expiring_certificates(config.EMAIL_MAP)
