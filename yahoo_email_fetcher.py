import os
import imaplib
import email
import requests

from email.header import decode_header
from email.utils import parseaddr
from dotenv import load_dotenv


load_dotenv()


# ---------------------------------------------------------
# YAHOO EMAIL CONFIGURATION
# ---------------------------------------------------------

YAHOO_EMAIL = os.getenv("YAHOO_EMAIL")
YAHOO_PASSWORD = os.getenv("YAHOO_PASSWORD")

YAHOO_IMAP_HOST = os.getenv(
    "YAHOO_IMAP_HOST",
    "imap.mail.yahoo.com"
)

YAHOO_IMAP_PORT = int(
    os.getenv("YAHOO_IMAP_PORT", "993")
)

ZOHO_FLOW_WEBHOOK_URL = os.getenv(
    "ZOHO_FLOW_WEBHOOK_URL"
)


# ---------------------------------------------------------
# EMAIL FILTER
# ---------------------------------------------------------

def should_process_email(sender, subject):

    sender = sender.lower()
    subject = subject.lower()

    blocked_senders = [
        "no-reply@zohopayroll.com",
        "teamzoom@e.zoom.us",
        "pinterest.com",
        "dubizzle.com"
    ]

    for blocked in blocked_senders:

        if blocked in sender:
            return False

    return True


# ---------------------------------------------------------
# DECODE EMAIL HEADER
# ---------------------------------------------------------

def decode_text(value):

    if not value:
        return ""

    decoded_parts = decode_header(value)

    result = ""

    for decoded, encoding in decoded_parts:

        if isinstance(decoded, bytes):

            result += decoded.decode(
                encoding or "utf-8",
                errors="ignore"
            )

        else:

            result += decoded

    return result.strip()


# ---------------------------------------------------------
# GET EMAIL BODY
# ---------------------------------------------------------

def get_email_body(msg):

    plain_body = ""
    html_body = ""

    if msg.is_multipart():

        for part in msg.walk():

            content_type = part.get_content_type()

            content_disposition = str(
                part.get("Content-Disposition")
            )

            # Ignore attachments
            if "attachment" in content_disposition.lower():
                continue

            payload = part.get_payload(
                decode=True
            )

            if not payload:
                continue

            charset = (
                part.get_content_charset()
                or "utf-8"
            )

            try:

                decoded = payload.decode(
                    charset,
                    errors="ignore"
                )

            except:

                decoded = payload.decode(
                    "utf-8",
                    errors="ignore"
                )

            if content_type == "text/plain":

                plain_body += decoded

            elif content_type == "text/html":

                html_body += decoded

    else:

        payload = msg.get_payload(
            decode=True
        )

        if payload:

            charset = (
                msg.get_content_charset()
                or "utf-8"
            )

            try:

                body = payload.decode(
                    charset,
                    errors="ignore"
                )

            except:

                body = payload.decode(
                    "utf-8",
                    errors="ignore"
                )

            if msg.get_content_type() == "text/html":

                html_body = body

            else:

                plain_body = body

    # Prefer plain text
    if plain_body.strip():

        return plain_body.strip()

    return html_body.strip()


# ---------------------------------------------------------
# SEND EMAIL TO ZOHO FLOW
# ---------------------------------------------------------

def send_to_zoho_flow(email_data):

    if not ZOHO_FLOW_WEBHOOK_URL:

        print(
            "ERROR: ZOHO_FLOW_WEBHOOK_URL is missing."
        )

        return False

    payload = {

        "source_mailbox": "yahoo",

        "date": email_data["date"],

        "subject": email_data["subject"],

        "from": email_data["from"],

        "from_name": email_data.get(
            "from_name",
            ""
        ),

        "body": email_data["body"]
    }

    print(
        "\nSENDING TO ZOHO FLOW:"
    )

    print(
        "From:",
        email_data["from"]
    )

    print(
        "From Name:",
        email_data.get(
            "from_name",
            ""
        )
    )

    print(
        "Subject:",
        email_data["subject"]
    )

    try:

        response = requests.post(

            ZOHO_FLOW_WEBHOOK_URL,

            json=payload,

            timeout=30
        )

        print(
            "ZOHO FLOW STATUS:",
            response.status_code
        )

        print(
            "ZOHO FLOW RESPONSE:",
            response.text
        )

        return response.status_code == 200

    except Exception as e:

        print(
            "Webhook Error:",
            e
        )

        return False


# ---------------------------------------------------------
# FETCH UNREAD YAHOO EMAILS
# ---------------------------------------------------------

def fetch_unread_emails():

    print(
        "Connecting to:",
        YAHOO_IMAP_HOST
    )

    mail = imaplib.IMAP4_SSL(

        YAHOO_IMAP_HOST,

        YAHOO_IMAP_PORT
    )

    mail.login(

        YAHOO_EMAIL,

        YAHOO_PASSWORD
    )

    print(
        "YAHOO LOGIN SUCCESSFUL!"
    )

    mail.select(
        "INBOX"
    )

    status, messages = mail.search(

        None,

        "UNSEEN"
    )

    if status != "OK":

        print(
            "Unable to search emails"
        )

        mail.logout()

        return []

    email_ids = messages[0].split()

    print(
        "Yahoo unread emails:",
        len(email_ids)
    )

    emails = []

    for email_id in email_ids:

        try:

            status, data = mail.fetch(

                email_id,

                "(RFC822)"
            )

            if status != "OK":

                continue

            raw_email = data[0][1]

            msg = email.message_from_bytes(
                raw_email
            )

            # -----------------------------
            # Sender
            # -----------------------------

            sender_header = decode_text(
                msg.get("From")
            )

            from_name, from_email = parseaddr(
                sender_header
            )

            from_name = from_name.strip()

            from_email = from_email.strip()

            # -----------------------------
            # Subject
            # -----------------------------

            subject = decode_text(
                msg.get("Subject")
            )

            # -----------------------------
            # Filter
            # -----------------------------

            if not should_process_email(

                sender_header,

                subject
            ):

                print(

                    "SKIPPED:",

                    from_email,

                    "|",

                    subject
                )

                mail.store(

                    email_id,

                    "+FLAGS",

                    "\\Seen"
                )

                continue

            # -----------------------------
            # Date
            # -----------------------------

            date = msg.get(
                "Date"
            )

            # -----------------------------
            # Body
            # -----------------------------

            body = get_email_body(
                msg
            )

            # -----------------------------
            # Email Data
            # -----------------------------

            email_data = {

                "email_id":
                    email_id.decode(),

                "from":
                    from_email,

                "from_name":
                    from_name,

                "subject":
                    subject,

                "date":
                    date,

                "body":
                    body
            }

            emails.append(
                email_data
            )

        except Exception as e:

            print(

                "Error processing email:",

                email_id,

                e
            )

    mail.logout()

    return emails


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":

    emails = fetch_unread_emails()

    print(
        "\n" + "=" * 60
    )

    if not emails:

        print(
            "No new emails to process."
        )

    for item in emails:

        print(

            "\nEMAIL ID:",

            item["email_id"]
        )

        print(

            "FROM:",

            item["from"]
        )

        print(

            "FROM NAME:",

            item["from_name"]
        )

        print(

            "SUBJECT:",

            item["subject"]
        )

        print(

            "DATE:",

            item["date"]
        )

        print(
            "\nBODY:"
        )

        print(

            item["body"][:1000]
        )

        print(
            "=" * 60
        )

        # ---------------------------------
        # Send to Zoho Flow
        # ---------------------------------

        success = send_to_zoho_flow(
            item
        )

        # ---------------------------------
        # Mark as processed
        # ---------------------------------

        if success:

            print(

                "SUCCESS: Email sent to Zoho Flow."
            )

            print(

                "Email ID:",

                item["email_id"],

                "will be marked as processed."
            )

            # Yahoo email marked as Seen
            # only after successful webhook

        else:

            print(

                "FAILED: Email was NOT marked as processed."
            )