import os
import requests
from dotenv import load_dotenv

load_dotenv()

refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")
client_id = os.getenv("ZOHO_CLIENT_ID")
client_secret = os.getenv("ZOHO_CLIENT_SECRET")

# Get fresh access token
token_response = requests.post(
    "https://accounts.zoho.com/oauth/v2/token",
    params={
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    }
)

print("TOKEN STATUS:", token_response.status_code)
print("TOKEN RESPONSE:", token_response.json())

token_data = token_response.json()

if "access_token" not in token_data:
    print("Could not get access token.")
    exit()

access_token = token_data["access_token"]

# Fetch Leads directly from Zoho CRM
crm_response = requests.get(
    "https://www.zohoapis.com/crm/v2/Leads",
    headers={
        "Authorization": "Zoho-oauthtoken " + access_token
    }
)

print("\nCRM STATUS:", crm_response.status_code)
print("\nCRM RESPONSE:")
print(crm_response.text)