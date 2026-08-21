import imaplib

mail = imaplib.IMAP4_SSL("mail.coretrst.ae", 993)

mail.login(
    "campleasing@coretrst.ae",
    "YOUR_PASSWORD"
)

mail.select("INBOX.Sent")

status, data = mail.search(None, "ALL")

email_ids = data[0].split()

last_id = email_ids[-1]

status, data = mail.fetch(
    last_id,
    "(INTERNALDATE BODY.PEEK[HEADER.FIELDS (DATE SUBJECT TO FROM)])"
)

print(data)

mail.logout()