from fastapi import APIRouter, Request, status
from authentication.auth import Auth
from database.schema import Student
from client.response import CustomResponse
from utils.query import LoginSchema
from exceptions.custom_exception import BadRequestException


router = APIRouter(tags=["Auth"], prefix="/auth")



auth = Auth()


@router.post("/login/student")
async def login_student(request: Request, login_input: LoginSchema):

    token = await auth.authenticate_student(login_input)

    context = {"token": token}

    return CustomResponse("login user successfully", data=context)







@router.post("/login/admin")
async def login_admin(request: Request, login_input: LoginSchema):

    token = await auth.authenticate_admin(login_input)

    context = {"token": token}

    return CustomResponse("login user successfully", data=context)