import os
import imaplib
import smtplib

from datetime import datetime, timezone
from dotenv import load_dotenv
from email.message import EmailMessage
from email.utils import format_datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

YAHOO_EMAIL = os.getenv("YAHOO_EMAIL")
YAHOO_PASSWORD = os.getenv("YAHOO_PASSWORD")
YAHOO_IMAP_HOST = os.getenv("YAHOO_IMAP_HOST", "imap.mail.yahoo.com")
YAHOO_IMAP_PORT = int(os.getenv("YAHOO_IMAP_PORT", "993"))
YAHOO_SMTP_HOST = os.getenv("YAHOO_SMTP_HOST", "smtp.mail.yahoo.com")
YAHOO_SMTP_PORT = int(os.getenv("YAHOO_SMTP_PORT", "465"))
YAHOO_SENT_FOLDER = os.getenv("YAHOO_SENT_FOLDER", "Sent")

app = FastAPI()


class EmailRequest(BaseModel):
    to: str
    subject: str
    body_html: str


def save_to_yahoo_sent(message, sent_time):
    imap = imaplib.IMAP4_SSL(YAHOO_IMAP_HOST, YAHOO_IMAP_PORT)

    try:
        imap.login(YAHOO_EMAIL, YAHOO_PASSWORD)

        status, response = imap.append(
            YAHOO_SENT_FOLDER,
            None,
            imaplib.Time2Internaldate(sent_time.timestamp()),
            message.as_bytes()
        )

        print("YAHOO SENT FOLDER STATUS:", status)
        print("YAHOO SENT FOLDER RESPONSE:", response)

        return status == "OK"

    finally:
        imap.logout()


@app.get("/")
def home():
    return {"status": "Yahoo Email Sender API is running"}


@app.post("/send-email")
def send_yahoo_email(data: EmailRequest):
    try:
        sent_time = datetime.now(timezone.utc)

        message = EmailMessage()
        message["From"] = YAHOO_EMAIL
        message["To"] = data.to
        message["Subject"] = data.subject
        message["Date"] = format_datetime(sent_time)

        message.set_content("Please view this email in HTML format.")
        message.add_alternative(data.body_html, subtype="html")

        with smtplib.SMTP_SSL(
            YAHOO_SMTP_HOST,
            YAHOO_SMTP_PORT
        ) as smtp:
            smtp.login(YAHOO_EMAIL, YAHOO_PASSWORD)
            smtp.send_message(message)

        print("SUCCESS: Yahoo email sent to recipient")

        sent_folder_saved = save_to_yahoo_sent(message, sent_time)

        return {
            "status": "success",
            "message": "Yahoo email sent successfully",
            "sent_folder_saved": sent_folder_saved,
            "to": data.to
        }

    except Exception as error:
        print("YAHOO SENDING ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )