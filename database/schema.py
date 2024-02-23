from mongoengine import Document, StringField, EmailField, DateTimeField, URLField, ReferenceField
from datetime import datetime




class Department(Document):

    department_name = StringField(required=True)

    department_image = URLField(required=True, default="www.google.com")





class Student(Document):

    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    email = EmailField(required=True, unique=True)

    password = StringField(required=True)

    department = ReferenceField(Department, required=True)

    created_at = DateTimeField(default=datetime.now())

    updated_at = DateTimeField(default=datetime.now())

    meta = {"collection": "users", "strict": False}


    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email, 
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
    




class Election(Document):

    election_name = StringField(required=True)

    election_image = URLField(required=False, default=None)

    department = ReferenceField(Department, required=True)
