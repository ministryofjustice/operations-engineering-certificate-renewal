import sys

from app.config import config
from app.services.NotifyService import NotifyService


def main(testrun: bool = False, test_email: str = ""):
    notify_service = NotifyService(
        config,
        config['keys']['notify_api_key'])

    print("Building undelivered email report...")
    undelivered_email_report = notify_service.check_for_undelivered_emails_for_template(
        config['template_ids']['cert_expiry'])

    print(f"Undelivered emails: {undelivered_email_report}")

    if len(undelivered_email_report) == 0:
        print("No undeliverable emails found, nice!")

    elif testrun:
        print(f"Sending test undelivered email report to {test_email}...")
        notify_service.send_report_email(
            notify_service.build_undeliverable_email_report_string(
                undelivered_email_report), config['template_ids']['undelivered_report'], test_email)
    else:
        print("Sending live report to Operations Engineering...")
        notify_service.send_report_email(
            notify_service.build_undeliverable_email_report_string(
                undelivered_email_report), config['template_ids']['undelivered_report'], config['reply_email'])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '-test':
        if len(sys.argv) > 2:
            main(True, sys.argv[2])
        else:
            raise SystemExit('Email address of recipient expected.')
    else:
        main()
