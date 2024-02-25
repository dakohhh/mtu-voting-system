import asyncio
from pydantic import EmailStr
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from authentication.auth import Auth
from authentication.hashing import checkPassword, hashPassword
from client.response import CustomResponse
from database.schema import Student
from repository.department import DepartmentRepository
from repository.otp import OTPRespository
from repository.student import StudentRepository
from utils.func import generate_random_otp
from utils.query import SignupSchema
from exceptions.custom_exception import BadRequestException
from utils.task import send_otp_mail


router = APIRouter(tags=["Student"], prefix="/student")


auth = Auth()


@router.post("/signup")
async def signup_student(request: Request, signup_input: SignupSchema):

    tasks = [
        StudentRepository.does_student_email_exits(signup_input.email),
        DepartmentRepository.does_department_exist(signup_input.department),
    ]

    (
        email_exits,
        department_exist,
    ) = await asyncio.gather(*tasks)

    if email_exits:

        raise BadRequestException("email already exists")

    if not department_exist:

        raise BadRequestException("department does not exists")

    student = await StudentRepository.create_student(signup_input)

    context = {"student": student.to_dict()}

    return CustomResponse("signup student successfully", data=context)



@router.post("/send_voting_number")
async def send_voting_number(request: Request, student:Student=Depends(auth.get_current_student)):





    context = {"student": student.to_dict()}

    return CustomResponse("signup student successfully", data=context)


    





@router.post("/request_otp")
async def request_otp(
    request: Request, email: EmailStr, background_task: BackgroundTasks
):

    student = await StudentRepository.get_student_by_email(email)

    if student is None:
        raise BadRequestException("this email doesn't exists")

    otp = generate_random_otp()

    if await OTPRespository.does_otp_exist(student):

        await OTPRespository.update_otp(student, hashPassword(str(otp)))

    else:
        await OTPRespository.create_otp(student, hashPassword(str(otp)))


    background_task.add_task(send_otp_mail, student, otp)

    return CustomResponse("sent otp successfully", data={"otp": str(otp)})


@router.post("/verify")
async def verify_student(request: Request, email: EmailStr, otp: str):

    student = await StudentRepository.get_student_by_email(email)

    if student is None:
        raise BadRequestException("this email doesn't exists")

    hash_otp = await OTPRespository.get_otp(student)

    if hash_otp is None or not checkPassword(otp, hash_otp.otp):
        raise BadRequestException("Invalid OTP")

    student.is_verified = True

    student.save()

    hash_otp.delete()

    context = {"student": student.to_dict()}

    return CustomResponse("student verified successfully", data=context)
