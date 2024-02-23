from database.schema import Student
from authentication.hashing import hashPassword
from utils.query import SignupSchema
import typing


class StudentRepository:

    @staticmethod
    async def create_student(student: SignupSchema):

        query = Student(
            firstname=student.firstname,
            lastname=student.lastname,
            password=hashPassword(student.password),
            email=student.email,
            department=student.department,
        )

        query.save()

        return query

    @staticmethod
    async def does_student_email_exits(email: str) -> bool:

        query = Student.objects(email=email).first()

        return query is not None

    @staticmethod
    async def get_student_by_email(email: str) -> typing.Union[Student, None]:

        query = Student.objects(email=email).first()

        return query

    @staticmethod
    async def get_student_by_id(student_id: str) -> typing.Union[Student, None]:

        query = Student.objects(id=student_id).first()

        return query