import os
import requests
from dotenv import load_dotenv

load_dotenv()

webhook_url = os.getenv("ZOHO_FLOW_WEBHOOK_URL")

payload = {
    "date": "2026-08-14",
    "subject": "AI Automation Test",
    "from": "saifur.rahman@pearlorganisation.com",
    "from_name": "Saifur Rahman",
    "body": "This is a test email for AI automation."
}

response = requests.post(
    webhook_url,
    json=payload,
    timeout=30
)

print("STATUS:", response.status_code)
print("RESPONSE:", response.text)