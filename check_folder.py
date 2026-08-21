import imaplib

mail = imaplib.IMAP4_SSL("mail.coretrst.ae", 993)
mail.login("YOUR_EMAIL", "YOUR_PASSWORD")

status, folders = mail.list()

for folder in folders:
    print(folder.decode(errors="ignore"))

mail.logout()