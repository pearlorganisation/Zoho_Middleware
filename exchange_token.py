import requests
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
REDIRECT_URI = os.getenv("ZOHO_REDIRECT_URI")

AUTHORIZATION_CODE = input("Paste your authorization code: ")

# url = "https://accounts.zoho.in/oauth/v2/token"
url = "https://accounts.zoho.com/oauth/v2/token"

data = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code": AUTHORIZATION_CODE
}

response = requests.post(url, data=data)

print("Status:", response.status_code)
print("Response:", response.json())