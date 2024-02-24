from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl
from beanie import PydanticObjectId
from datetime import datetime


class LoginSchema(BaseModel):

    email: EmailStr

    password: str

    department: PydanticObjectId





class SignupSchema(BaseModel):

    firstname: str
    
    lastname: str

    password: str

    email: EmailStr

    department: PydanticObjectId




class DepartmentSchema(BaseModel):

    department_name:str

    department_image: Optional[HttpUrl] = None




class AdminSchema(BaseModel):

    email: EmailStr

    password: str

    department: PydanticObjectId




class Token(BaseModel):
    user: str
    exp: int

    def get_expiry_time(self):
        return datetime.utcfromtimestamp(self.exp)
