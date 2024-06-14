from fastapi import APIRouter, Request
from authentication.auth import Auth
from client.response import CustomResponse
from utils.query import LoginSchema


router = APIRouter(tags=["Auth"], prefix="/auth")



auth = Auth()


@router.post("/login/student")
async def login_student(request: Request, login_input: LoginSchema):

    user, token = await auth.authenticate_student(login_input)

    context = {"user": user.to_dict(), "token": token}

    return CustomResponse("login user successfully", data=context)





@router.post("/login/admin")
async def login_admin(request: Request, login_input: LoginSchema):

    user, token = await auth.authenticate_admin(login_input)


    context = {"user": user.to_dict(), "token": token}

    return CustomResponse("login user successfully", data=context)