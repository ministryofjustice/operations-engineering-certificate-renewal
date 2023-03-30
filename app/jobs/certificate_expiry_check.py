from app.config import config
from app.services.GandiService import GandiService
from app.services.NotifyService import NotifyService
from app.services.S3Service import S3Service


def main():
    # Instantiate services
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
    email_mappings = s3_service.get_json_file(
        config['s3']['s3_bucket_name'],
        config['s3']['s3_object_name'],
        './app/s3_email_mapping.json')

    # Get a list of the expired certificates from Gandi
    certificate_list = gandi_service.get_certificate_list()
    valid_certificate_list = gandi_service.get_certificates_in_valid_state(
        certificate_list, email_mappings)
    expired_certificate_list = gandi_service.get_expired_certificates_from_valid_certificate_list(
        valid_certificate_list, email_mappings
    )

    # Build parameters to send emails
    email_parameter_list = notify_service.build_email_parameter_list(
        expired_certificate_list)

    # Send emails for the expired certificates using Notify
    notify_service.send_emails_from_parameters(email_parameter_list)

    # Send report email to OE
    # TODO


if __name__ == "__main__":
    main()
