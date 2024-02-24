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
            "department": str(self.department.id),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }




class Election(Document):

    election_name = StringField(required=True)

    election_image = URLField(required=False, default=None)

    department = ReferenceField(Department, required=True)


class EmailOTP(Document):

    otp = StringField(required=True)

    student = ReferenceField(Student, required=True)
