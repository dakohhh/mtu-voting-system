import asyncio
from fastapi import UploadFile
from fastapi_mail import FastMail
from database.schema import Candidate, Election, Student
from utils.mail import conf, get_otp_message_schema
from utils.upload import MTUVoteUpload





async def send_otp_mail(student:Student, otp:str):

    
    message = get_otp_message_schema(student, otp)

    mail = FastMail(conf)

    asyncio.create_task(mail.send_message(message))




def save_election_image(election:Election, uploader:MTUVoteUpload, image:UploadFile):

    metadata = uploader.handle_upload(image)

    election.election_image = metadata["secure_url"]

    election.save()



def save_candidate_image(candidate:Candidate, uploader:MTUVoteUpload, image:UploadFile):

    metadata = uploader.handle_upload(image)

    candidate.candidate_image = metadata["secure_url"]

    candidate.save()