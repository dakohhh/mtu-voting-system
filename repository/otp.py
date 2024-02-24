import typing
from database.schema import EmailOTP, Student
from utils.func import generate_random_otp
from authentication.hashing import hashPassword


class OTPRespository:

    @staticmethod
    async def create_otp(student: Student, hash_otp: str):

        query = EmailOTP(otp=hash_otp, student=student)

        query.save()

    @staticmethod
    async def does_otp_exist(student: Student) -> bool:

        query = EmailOTP.objects(student=student).first()

        return query is not None

    @staticmethod
    async def update_otp(student: Student, hash_otp: str) -> bool:

        query: EmailOTP = EmailOTP.objects(student=student).first()

        query.otp = hash_otp

        query.save()

    @staticmethod
    async def get_otp(student: Student) -> typing.Union[EmailOTP, None]:

        query: EmailOTP = EmailOTP.objects(student=student).first()

        return query
