import os
import asyncio
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from dotenv import load_dotenv

load_dotenv()


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_USERNAME"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER="smtp.gmail.com",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
)


def get_notify_message_schema(
    emails: list, camera, time_of_detection, detected_user=None, link=None
):
    html = f"""
    <p>Hello user, we have noticed some suspicious detections from camera {camera}</p> 
    <p>Details Of Detections</p>
    ============================
    <br>
    Location: Camera {camera}
    <br>
    Time: {time_of_detection}
    <br>
    Source: {link}"""

    return MessageSchema(
        subject="We have detected movements!",
        recipients=emails,
        body=html,
        subtype=MessageType.html,
    )
