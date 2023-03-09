import json
import os


DEFAULT_REPLY_EMAIL = "certificates@digital.justice.gov.uk"
CERT_EXPIRY_THRESHOLDS = [30, 15, 1]

NOTIFY_API_KEY = os.getenv('NOTIFY_API_KEY')
GANDI_API_KEY = os.getenv('GANDI_API_KEY')

# URLs
GANDI_BASE_URL = "https://api.gandi.net/"
CERT_URL_EXTENSION = "v5/certificate/issued-certs"

# Email Template IDs
CERT_EXPIRE_EMAIL_TEMPLATE_ID = "06abd028-0a8f-43d9-a122-90a92f9b62ee"

with open('resources/mappings.json') as file:
    mappings = file.read()
EMAIL_MAP = json.loads(mappings)
