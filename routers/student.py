import asyncio
from fastapi import APIRouter, Request, status
from authentication.auth import Auth
from database.schema import Department, Student
from client.response import CustomResponse
from repository.department import DepartmentRepository
from repository.student import StudentRepository
from utils.query import LoginSchema, SignupSchema
from exceptions.custom_exception import BadRequestException


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
    
    # context = {"user": }
    

    return CustomResponse("signup user successfully")
