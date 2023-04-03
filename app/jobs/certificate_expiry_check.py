import sys

from app.config import config
from app.services.GandiService import GandiService
from app.services.NotifyService import NotifyService
from app.services.S3Service import S3Service


def main(testrun: bool = False, test_email: str = ""):
    # Instantiate services
    print("Instantiating services...")
    s3_service = S3Service()
    gandi_service = GandiService(
        config,
        config['keys']['gandi_api_key'],
        config['urls']['gandi_base_url'],
        config['urls']['gandi_cert_url_extension'])
    notify_service = NotifyService(
        config,
        config['keys']['notify_api_key'])

    # Get a list of the email mappings from S3
    print("Extracting email map from S3")
    email_mappings = s3_service.get_json_file(
        config['s3']['s3_bucket_name'],
        config['s3']['s3_object_name'],
        './app/s3_email_mapping.json')

    # Get a list of the expired certificates from Gandi
    print("Extracting certificate list from Gandi...")
    certificate_list = gandi_service.get_certificate_list()
    valid_certificate_list = gandi_service.get_certificates_in_valid_state(
        certificate_list, email_mappings)
    expired_certificate_list = gandi_service.get_expired_certificates_from_valid_certificate_list(
        valid_certificate_list, email_mappings
    )

    # Build parameters to send emails
    print("Building parameters to send emails...")
    email_parameter_list = notify_service.build_email_parameter_list(
        expired_certificate_list)

    # Send emails for the expired certificates using Notify based on whether it's a test run or not
    if testrun:
        print("Sending test email report...")
        notify_service.send_test_email_from_parameters(
            email_parameter_list, test_email)
    else:
        print("Sending live emails...")
        notify_service.send_emails_from_parameters(email_parameter_list)

    # Send report email to OE
    notify_service.send_report_email_to_operations_engineering(
        email_parameter_list)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '-test':
        if len(sys.argv) > 2:
            main(True, sys.argv[2])
        else:
            raise SystemExit('Email address of recipient expected.')
    else:
        main()
