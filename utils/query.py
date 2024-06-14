from typing import List, Optional
from fastapi import Form, UploadFile, File
from pydantic import BaseModel, EmailStr, HttpUrl
from beanie import PydanticObjectId
from datetime import datetime


class LoginSchema(BaseModel):

    email: EmailStr

    password: str


class SignupSchema(BaseModel):

    firstname: str

    lastname: str

    password: str

    email: EmailStr

    department_id: PydanticObjectId


class DepartmentSchema(BaseModel):

    department_name: str

    department_image: Optional[HttpUrl] = None


class AdminSchema(BaseModel):

    email: EmailStr

    password: str

    department_id: PydanticObjectId




class CreateElectionSchema:
    def __init__(
        self,
        election_name: str,
        election_image: UploadFile = File(None),
    ):
        self.election_name = election_name
        self.election_image = election_image





class CreateCandidateSchema:
    def __init__(
        self,
        candidate_name: str = Form(...),
        election_id: PydanticObjectId = Form(...),
        candidate_image: UploadFile = File(None),
    ):
        self.candidate_name = candidate_name
        self.election_id = election_id
        self.candidate_image = candidate_image



class VoteSchema(BaseModel):

    candidate_id: PydanticObjectId

    election_id: PydanticObjectId




class Token(BaseModel):
    user: str
    exp: int

    def get_expiry_time(self):
        return datetime.utcfromtimestamp(self.exp)
