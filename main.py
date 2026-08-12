from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os
from urllib.parse import urlencode

load_dotenv()

app = FastAPI()

CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
REDIRECT_URI = os.getenv("ZOHO_REDIRECT_URI")

@app.get("/")
def home():
    return {"message": "Zoho Middleware is running"}

@app.get("/login")
def login():

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "access_type": "offline",
        "redirect_uri": REDIRECT_URI,
        "scope": "ZohoCRM.modules.ALL,ZohoCRM.settings.fields.ALL"
    }

    url = "https://accounts.zoho.in/oauth/v2/auth?" + urlencode(params)

    return RedirectResponse(url)


@app.get("/oauth/callback")
def oauth_callback(code: str):

    return {
        "message": "Zoho authorization successful",
        "authorization_code": code
    }