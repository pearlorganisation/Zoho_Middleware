import os
import requests
from dotenv import load_dotenv

load_dotenv()

refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")
client_id = os.getenv("ZOHO_CLIENT_ID")
client_secret = os.getenv("ZOHO_CLIENT_SECRET")

# Get access token
token_response = requests.post(
    "https://accounts.zoho.com/oauth/v2/token",
    params={
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    }
)

token_data = token_response.json()

if "access_token" not in token_data:
    print("Token Error:")
    print(token_data)
    exit()

access_token = token_data["access_token"]

# Lead ID
lead_id = "6761376000020406001"

# Get specific Lead
response = requests.get(
    f"https://www.zohoapis.com/crm/v2/Leads/{lead_id}",
    headers={
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }
)

print("STATUS:", response.status_code)
print("RESPONSE:")
print(response.text)