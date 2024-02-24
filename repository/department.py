from typing import List
from database.schema import Department
from utils.query import DepartmentSchema


class DepartmentRepository:

    @staticmethod
    async def does_department_exist(department_id: str) -> bool:

        query = Department.objects(id=department_id).first()

        return query is not None

    @staticmethod
    async def create_department(department_input: DepartmentSchema):

        query = Department(
            department_name=department_input.department_name,
            department_image=str(department_input.department_image),
        )


        query.save()

        return query
    


    @staticmethod
    async def get_all_departments() -> List[Department]:

        query = Department.objects().all()


        return query
