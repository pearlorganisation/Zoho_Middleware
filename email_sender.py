import os
import smtplib
import imaplib

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from email.message import EmailMessage
from email.utils import format_datetime
from datetime import datetime
from zoneinfo import ZoneInfo

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_USER = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))

app = FastAPI()


class EmailRequest(BaseModel):
    to: str
    subject: str
    body_html: str


@app.get("/")
def home():
    return {
        "status": "Email Sender API is running"
    }


def save_to_sent_folder(msg, sent_time):

    try:
        print("Connecting to IMAP for Sent folder...")

        imap = imaplib.IMAP4_SSL(EMAIL_HOST, 993)

        print("IMAP connection successful")

        imap.login(
            EMAIL_USER,
            EMAIL_PASSWORD
        )

        print("IMAP login successful")

        status, response = imap.append(
            "INBOX.Sent",
            None,
            imaplib.Time2Internaldate(sent_time),
            msg.as_bytes()
        )

        print("IMAP APPEND STATUS:", status)
        print("IMAP APPEND RESPONSE:", response)

        imap.logout()

        if status == "OK":
            print("SUCCESS: Email saved to INBOX.Sent")
            return True

        print("FAILED: Email was NOT saved to INBOX.Sent")
        return False

    except Exception as e:
        print("Sent folder error:", repr(e))
        return False

@app.post("/send-email")
def send_email(data: EmailRequest):

    try:

        msg = EmailMessage()

        msg["From"] = EMAIL_USER
        msg["To"] = data.to
        msg["Subject"] = data.subject
        # msg["Date"] = format_datetime(datetime.now(timezone.utc))
        uae_time = datetime.now(ZoneInfo("Asia/Dubai"))
        msg["Date"] = format_datetime(uae_time)
        
        msg.set_content(
            "Please view this email in HTML format."
        )

        msg.add_alternative(
            data.body_html,
            subtype="html"
        )

        # ----------------------------------
        # SEND EMAIL
        # ----------------------------------

        print("Connecting to SMTP...")

        with smtplib.SMTP_SSL(
            SMTP_HOST,
            SMTP_PORT
        ) as smtp:

            smtp.login(
                EMAIL_USER,
                EMAIL_PASSWORD
            )
            
            
            smtp.send_message(msg)

        print(
            "SUCCESS: Email sent to recipient"
        )

        # ----------------------------------
        # SAVE COPY TO SENT
        # ----------------------------------

        sent_saved = save_to_sent_folder(msg, uae_time)

        if not sent_saved:

            print(
                "WARNING: Email was sent but "
                "Sent folder copy failed."
            )

        return {
            "status": "success",
            "message": "Email sent successfully",
            "sent_folder_saved": sent_saved,
            "to": data.to
        }

    except Exception as e:

        print(
            "EMAIL SENDING ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )