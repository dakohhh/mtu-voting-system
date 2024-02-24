import asyncio
from fastapi_mail import FastMail
from database.schema import Student
from utils.mail import conf, get_otp_message_schema





async def send_otp_mail(student:Student, otp:str):

    
    message = get_otp_message_schema(student, otp)

    mail = FastMail(conf)

    asyncio.create_task(mail.send_message(message))