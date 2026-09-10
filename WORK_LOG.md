# Zoho CRM AI Email Automation — Practical Work Log

1. **Email Fetcher and Zoho Flow webhook validation**  
   Fetched unread messages, confirmed IMAP login, displayed the email ID/sender/subject, and verified the Zoho Flow webhook returned HTTP 200.  
   **Screenshot:** Terminal after running `email_fetcher.py`, showing `LOGIN SUCCESSFUL!`, `Unread emails`, `EMAIL ID`, `FROM`, `SUBJECT`, `ZOHO FLOW STATUS: 200`, and `SUCCESS: Email sent to Zoho Flow.`

2. **Zoho Flow AI priority and urgency classification**  
   Enhanced the Zoho CRM AI Automation flow to classify the incoming email’s priority and urgency from its content.  
   **Screenshot:** Zoho Flow run history/details page showing the AI output fields for priority and urgency.

3. **Email Sender API webhook validation**  
   Validated the Zoho CRM AI Automation webhook API and the `/send-email` endpoint using dynamic recipient, subject, and HTML body parameters.  
   **Screenshot:** Postman/API client response showing `status: success` and `Email sent successfully`.

4. **Email Sender API delivery verification**  
   Tested SMTP delivery and confirmed the middleware returns a successful response after the message is sent to the recipient.  
   **Screenshot:** Terminal running the Email Sender API, showing `SUCCESS: Email sent to recipient`.

5. **Sent folder timestamp verification**  
   Saved the sent message through IMAP using the same UTC instant as its email `Date` header, preventing conflicting Sent-folder and received-message times.  
   **Screenshot:** Mail client’s Sent folder, with the sent message selected and its timestamp visible.

6. **Yahoo email-provider support**  
   Added Yahoo-ready environment configuration using `imap.mail.yahoo.com:993` and `smtp.mail.yahoo.com:465`; access must use a Yahoo App Password.  
   **Screenshot:** Local `.env` configuration (with the app password masked) or the `.env.example` file in the project.
