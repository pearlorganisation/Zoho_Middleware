from fastapi import FastAPI
from pydantic import BaseModel
from email_sender import send_actual_email

app = FastAPI()


class EmailRequest(BaseModel):

    to: str
    subject: str
    body_html: str


@app.post("/send-email")
def send_email(data: EmailRequest):

    success = send_actual_email(
        data.to,
        data.subject,
        data.body_html
    )

    if success:

        return {
            "status": "success",
            "message": "Email sent successfully"
        }

    return {
        "status": "error",
        "message": "Email sending failed"
    }