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
        await DepartmentRepository.does_department_exist(signup_input.department),
    ]

    (
        does_student_email_exits,
        does_department_exist,
    ) = await asyncio.gather(*tasks)

    if await does_student_email_exits:

        raise BadRequestException("email already exists")

    if not does_department_exist:

        raise BadRequestException("department does not already exists")
    

    


    return CustomResponse("login user successfully")
