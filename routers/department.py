from fastapi import APIRouter, Request, status
from authentication.auth import Auth
from database.schema import Department, Student
from client.response import CustomResponse
from utils.query import LoginSchema, DepartmentSchema
from exceptions.custom_exception import BadRequestException


router = APIRouter(tags=["Department"], prefix="/department")



auth = Auth()


@router.post("/create")
async def create_department(request: Request, secret:str, department_input:DepartmentSchema):

    if secret != "wisdom12":
        raise BadRequestException("invalid secrete")



    return CustomResponse("created department successfully")






