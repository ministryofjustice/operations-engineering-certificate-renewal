import datetime


class TestData:
    test_domain_name_root = "test.domain.gov.uk"
    test_recipient_email_root = "test.user@mail.com"
    test_recipientcc_email_root = "test.user.cc@mail.com"
    test_cname_email_root = "test.cname.user@mail.com"

    @classmethod
    def generate_single_email_list(cls, owner: str = 'OE', recipcc: int = 0, cname: int = 0):
        recipientcc = [f"{cls.test_recipientcc_email_root}{i}" for i in range(recipcc)]
        external_cname = [f"{cls.test_cname_email_root}{i}" for i in range(cname)]
        return {
            cls.test_domain_name_root: {
                "recipient": cls.test_recipient_email_root,
                "recipientcc": recipientcc,
                "owner": owner,
                "external_cname": external_cname,
            }
        }

    @classmethod
    def generate_multiple_email_list(cls, count: int = 1, owner: str = 'OE', recipcc: int = 0, cname: int = 0):
        recipientcc = [f"{cls.test_recipientcc_email_root}{i}" for i in range(recipcc)]
        external_cname = [f"{cls.test_cname_email_root}{i}" for i in range(cname)]
        return {
            f"{cls.test_domain_name_root}{i}": {
                "recipient": cls.test_recipient_email_root,
                "recipientcc": recipientcc,
                "owner": owner,
                "external_cname": external_cname,
            }
            for i in range(count)
        }

    @classmethod
    def generate_single_filtered_certificate_list_with_expiry_date(cls, days: int):
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=days)
        return {cls.test_domain_name_root: {"expiry_date": expiry_date}}

    @classmethod
    def generate_multiple_filtered_certificate_list_with_expiry_date(cls, days: int, count: int = 1):
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=days)
        return {
            f"{cls.test_domain_name_root}{i}": {"expiry_date": expiry_date}
            for i in range(count)
        }

    @classmethod
    def generate_single_gandi_certificate_state(cls, state: str):
        return [{"cn": cls.test_domain_name_root, "status": state,
                 "dates": {"ends_at": "2023-01-01T06:00:00Z"}, }]

    @classmethod
    def generate_multiple_gandi_certificate_states(cls, state: str, count: int = 1):
        return [
            {"cn": f"{cls.test_domain_name_root}{i}", "status": state,
             "dates": {"ends_at": "2023-01-01T06:00:00Z"}, }
            for i in range(count)]
