from mongoengine import (
    Document,
    StringField,
    EmailField,
    DateTimeField,
    URLField,
    ReferenceField,
    BooleanField,
)
from datetime import datetime


class Department(Document):

    department_name = StringField(required=True)

    department_image = URLField()

    def to_dict(self):

        return {
            "id": str(self.id),
            "department_name": self.department_name,
            "department_image": self.department_image,
        }


class Student(Document):

    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    email = EmailField(required=True, unique=True)

    password = StringField(required=True)

    department = ReferenceField(Department, required=True)

    is_verified = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.now())

    updated_at = DateTimeField(default=datetime.now())

    meta = {"strict": False}

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "role": "student",
            "email": self.email,
            "department": str(self.department.id),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class Admin(Document):

    email = EmailField(required=True, unique=True)

    password = StringField(required=True)

    department = ReferenceField(Department, required=True)

    created_at = DateTimeField(default=datetime.now())

    updated_at = DateTimeField(default=datetime.now())

    meta = {"strict": False}

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "email": self.email,
            "role": "admin",
            "department": str(self.department.id),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class Election(Document):

    election_name = StringField(required=True)

    department = ReferenceField(Department, required=True)

    election_image = URLField(required=False, default=None)

    def to_dict(self):

        return {
            "election_id": str(self.id),
            "election_name": self.election_name,
            "department": str(self.department.id),
            "election_image": self.election_image,
        }


class Candidate(Document):

    candidate_name = StringField(required=True)

    candidate_image = URLField(required=False, default=None)

    election = ReferenceField(Election, required=True)

    def to_dict(self):
        return {
            "candidate_id": str(self.id),
            "candidate_name": self.candidate_name,
            "election": str(self.election.id),
            "candidate_image": self.candidate_image,
        }


class Vote(Document):

    student = ReferenceField(Student, required=True)

    candidate = ReferenceField(Candidate, required=True)

    election = ReferenceField(Election, required=True)



class EmailOTP(Document):

    otp = StringField(required=True)

    student = ReferenceField(Student, required=True)
