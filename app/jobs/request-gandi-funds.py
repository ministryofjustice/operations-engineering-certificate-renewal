from app.config import config
from app.services.GandiService import GandiService
from app.services.NotifyService import NotifyService


def main():
    # Set up the services
    gandi_service = GandiService(
        config,
        config['keys']['gandi_api_key'],
        config['urls']['gandi_base_url'],
        config['urls']['gandi_billing_url_extension'])
    notify_service = NotifyService(
        config,
        config['keys']['notify_api_key'])

    # Get the current account amount from the organisation page and send emails:
    current_account_balance = gandi_service.get_current_account_balance_from_org(config['gandi']['gandi_org_id'])

    if current_account_balance < config['gandi']['balance_threshold']:
        notify_service.send_gandi_fund_request(
            config['template_ids']['request_gandi_funds'],
            config['gandi']['gandi_funds_email'],
            config['gandi']['topup_amount'],
            current_account_balance
        )
        notify_service.send_gandi_fund_report(
            config['template_ids']['request_gandi_funds_report'],
            config['reply_email'],
            config['gandi']['topup_amount'],
            current_account_balance
        )


if __name__ == "__main__":
    main()
