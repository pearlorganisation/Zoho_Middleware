import os
import requests
from dotenv import load_dotenv

load_dotenv()

refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")
client_id = os.getenv("ZOHO_CLIENT_ID")
client_secret = os.getenv("ZOHO_CLIENT_SECRET")

lead_id = "6761376000020406001"


# =========================
# 1. Get Access Token
# =========================

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


# =========================
# 2. Get Lead
# =========================

response = requests.get(
    f"https://www.zohoapis.com/crm/v2/Leads/{lead_id}",
    headers={
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }
)

print("STATUS:", response.status_code)

if response.status_code != 200:
    print("CRM Error:")
    print(response.text)
    exit()


# =========================
# 3. Read Lead Data
# =========================

response_data = response.json()

lead = response_data["data"][0]

print("\nLead Name:")
print(lead.get("Full_Name"))

print("\nEmail:")
print(lead.get("Email"))

print("\nAI Processed:")
print(lead.get("AI_Processed"))

print("\nAI Summary:")
print(lead.get("AI_Summary"))

print("\nAI Required Action:")
print(lead.get("AI_Required_Action"))

print("\nAI Draft Reply:")
print(lead.get("AI_Draft_Reply"))