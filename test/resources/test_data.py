import datetime


class TestData:
    test_domain_name = "test.domain.gov.uk"

    @classmethod
    def generate_valid_email_list(cls):
        return {
            cls.test_domain_name: {
                "recipient": "test.user@mail.com",
                "recipientcc": [],
                "owner": "OE",
                "external_cname": ["external.person@mail.com"],
            }
        }

    @classmethod
    def generate_filtered_certificate_list_with_expiry_date(cls, days: int):
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=days)
        return {cls.test_domain_name: {'expiry_date': expiry_date}}

    @classmethod
    def generate_gandi_certificate_state(cls, state: str):
        return [{"cn": cls.test_domain_name, "status": state, "dates": {"ends_at": "2023-01-01T06:00:00Z"}}]
