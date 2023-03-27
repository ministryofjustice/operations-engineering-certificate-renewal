import datetime


class TestData:
    test_domain_name_root = "test.domain.gov.uk"

    @classmethod
    def generate_single_email_list(cls, owner: str = 'OE'):
        return {
            cls.test_domain_name_root: {
                "recipient": "test.user@mail.com",
                "recipientcc": [],
                "owner": owner,
                "external_cname": ["external.person@mail.com"],
            }
        }

    @classmethod
    def generate_multiple_email_list(cls, count: int = 1, owner: str = 'OE'):
        return {
            cls.test_domain_name_root + str(i): {
                "recipient": "test.user@mail.com",
                "recipientcc": [],
                "owner": owner,
                "external_cname": ["external.person@mail.com"],
            }
            for i in range(count)
        }

    @classmethod
    def generate_filtered_certificate_list_with_expiry_date(cls, days: int):
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=days)
        return {cls.test_domain_name_root: {"expiry_date": expiry_date}}

    @classmethod
    def generate_single_gandi_certificate_state(cls, state: str):
        return [{"cn": cls.test_domain_name_root, "status": state,
                 "dates": {"ends_at": "2023-01-01T06:00:00Z"}, }]

    @classmethod
    def generate_multiple_gandi_certificate_states(cls, state: str, count: int = 1):
        return [
            {"cn": cls.test_domain_name_root + str(i), "status": state,
             "dates": {"ends_at": "2023-01-01T06:00:00Z"}, }
            for i in range(count)]
