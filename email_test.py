import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 993))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def decode_text(value):
    if not value:
        return ""

    decoded = decode_header(value)
    result = ""

    for text, encoding in decoded:
        if isinstance(text, bytes):
            result += text.decode(encoding or "utf-8", errors="ignore")
        else:
            result += text

    return result


print("Connecting to:", EMAIL_HOST)

try:
    mail = imaplib.IMAP4_SSL(EMAIL_HOST, EMAIL_PORT)

    mail.login(EMAIL_USERNAME, EMAIL_PASSWORD)

    print("LOGIN SUCCESSFUL!")

    mail.select("INBOX")

    status, messages = mail.search(None, "ALL")

    if status != "OK":
        print("Could not read inbox.")
        exit()

    email_ids = messages[0].split()

    print("Total emails:", len(email_ids))

    # Latest 5 emails
    latest_emails = email_ids[-5:]

    for email_id in reversed(latest_emails):

        status, data = mail.fetch(email_id, "(RFC822)")

        if status != "OK":
            continue

        raw_email = data[0][1]

        msg = email.message_from_bytes(raw_email)

        subject = decode_text(msg.get("Subject"))
        sender = decode_text(msg.get("From"))
        date = msg.get("Date")

        print("\n" + "=" * 60)
        print("FROM:", sender)
        print("SUBJECT:", subject)
        print("DATE:", date)

        # Get email body
        body = ""

        if msg.is_multipart():

            for part in msg.walk():

                content_type = part.get_content_type()
                content_disposition = str(
                    part.get("Content-Disposition")
                )

                if content_type == "text/plain" and "attachment" not in content_disposition:

                    payload = part.get_payload(decode=True)

                    if payload:
                        body = payload.decode(
                            part.get_content_charset() or "utf-8",
                            errors="ignore"
                        )

                        break

        else:

            payload = msg.get_payload(decode=True)

            if payload:
                body = payload.decode(
                    msg.get_content_charset() or "utf-8",
                    errors="ignore"
                )

        print("BODY:")
        print(body[:2000])

    mail.logout()

    print("\nEmail fetching completed successfully!")

except Exception as e:

    print("\nERROR:")
    print(type(e).__name__, "-", str(e))