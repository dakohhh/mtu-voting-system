from fastapi import APIRouter, Request, status
from authentication.auth import Auth
from database.schema import Student
from client.response import CustomResponse
from repository.admin import AdminRepository
from utils.query import AdminSchema, LoginSchema
from exceptions.custom_exception import BadRequestException


router = APIRouter(tags=["Admin"], prefix="/admin")



auth = Auth()


@router.post("/create")
async def create_admin(request: Request, secret:str, admin_input:AdminSchema):

    if secret != "wisdom12":
        raise BadRequestException("incorrect secret")
    

    if await AdminRepository.does_admin_exist(admin_input.email):

        raise BadRequestException("The email already exists")
    
    
    admin = await AdminRepository.create_admin(admin_input)

    context = {"admin": admin.to_dict()}

    return CustomResponse("login user successfully", data=context)




