
from database.schema import Department


class DepartmentRepository():


    @staticmethod
    async def does_department_exist(department_id:str) -> bool:

        query = Department.objects(id=department_id).first()


        return query is not None

