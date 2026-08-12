import os
import requests
from dotenv import load_dotenv

load_dotenv()

refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")
client_id = os.getenv("ZOHO_CLIENT_ID")
client_secret = os.getenv("ZOHO_CLIENT_SECRET")

lead_id = "6761376000020406001"


# =========================
# 1. Get Fresh Access Token
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

if response.status_code != 200:
    print("CRM Error:")
    print(response.text)
    exit()

lead = response.json()["data"][0]


# =========================
# 3. Check AI Processed
# =========================

ai_processed = lead.get("AI_Processed")

print("Lead:", lead.get("Full_Name"))
print("AI_Processed:", ai_processed)


if ai_processed is True:
    print("\nLead already processed.")
    exit()


if ai_processed is not False:
    print("\nAI_Processed value is missing or invalid.")
    exit()


# =========================
# 4. Prepare AI Input
# =========================

ai_input = {
    "sender_name": lead.get("First_Name"),
    "sender_email": lead.get("Email"),
    "inquiry_type": lead.get("Inquiry_Type"),
    "urgency": lead.get("Inquiry_Urgency"),
    "summary": lead.get("AI_Summary"),
    "required_action": lead.get("AI_Required_Action"),
    "draft_reply": lead.get("AI_Draft_Reply"),
    "description": lead.get("Description")
}


# =========================
# 5. Display AI Input
# =========================

print("\n========== AI INPUT ==========")

for key, value in ai_input.items():
    print(f"{key}: {value}")

print("==============================")

print("\nLead is ready to be sent to AI.")