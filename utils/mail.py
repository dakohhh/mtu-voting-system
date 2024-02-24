import os
import asyncio
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from dotenv import load_dotenv
from database.schema import Student

load_dotenv()


conf = ConnectionConfig(
    MAIL_USERNAME= os.getenv("MAIL_USERNAME"), 
    MAIL_PASSWORD= os.getenv("MAIL_PASSWORD"), 
    MAIL_FROM= os.getenv("MAIL_USERNAME"), 
    MAIL_FROM_NAME= "MTU VOTE", 
    MAIL_PORT= int(os.getenv("MAIL_PORT")),
    MAIL_SERVER="smtp.gmail.com" , 
    USE_CREDENTIALS= True, 
    VALIDATE_CERTS = True,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,

)



def get_otp_message_schema(student:Student, otp:str):



    html = f'''<div style="text-align: center;">
            <img src="https://res.cloudinary.com/marvel6/image/upload/v1681901707/chow_qjjtro.jpg" alt="Company Logo" style="border-radius: 50%; width: 200px; height: 200px; object-fit: cover; margin-top: 20px;">
        </div>
        <p style="font-size: 16px; margin-bottom: 20px;">Dear {student.firstname} {student.lastname} ,</p>
        <p style="font-size: 16px; margin-bottom: 20px;">Your OTP is  {otp}.</p>
        <p style="font-size: 16px; margin-bottom: 20px;">Thank you! :-)</p>
        <p style="font-size: 16px; margin-bottom: 0;">MTU VOTE </p>
    </div>'''

    return MessageSchema(
        subject=f"Your OTP for verification!",
        recipients=[student.email],
        body=html,
        subtype=MessageType.html
    )
