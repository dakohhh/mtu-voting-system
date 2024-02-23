from pydantic import BaseModel, EmailStr
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

    email: str

    department: PydanticObjectId



class Token(BaseModel):
    user: str
    exp: int

    def get_expiry_time(self):
        return datetime.utcfromtimestamp(self.exp)
