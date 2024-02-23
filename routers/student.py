import asyncio
from fastapi import APIRouter, Request, status
from authentication.auth import Auth
from database.schema import Department, Student
from client.response import CustomResponse
from repository.student import StudentRepository
from utils.query import LoginSchema, SignupSchema
from exceptions.custom_exception import BadRequestException


router = APIRouter(tags=["Student"], prefix="/student")


auth = Auth()




@router.post("/signup")
async def signup_student(request: Request, signup_input: SignupSchema):


    

    if await StudentRepository.does_student_email_exits(signup_input.email):

        raise BadRequestException("email already exists")
        

    

    context = {"token": "wd"}

    return CustomResponse("login user successfully", data=context)




