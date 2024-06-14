import typing
from authentication.hashing import hashPassword
from database.schema import Admin
from utils.query import AdminSchema


class AdminRepository:

    @staticmethod
    async def create_admin(admin_input: AdminSchema):

        query = Admin(
            email=admin_input.email,
            password=hashPassword(admin_input.password),
            department=admin_input.department_id,
        )

        query.save()

        return query
    


    @staticmethod
    async def does_admin_exist(email:str) -> bool:

        query = Admin.objects(email=email).first()


        return query is not None
    

    @staticmethod
    async def get_admin_by_email(email: str) -> typing.Union[Admin, None]:


        query = Admin.objects(email=email).first()

        return query
    


    @staticmethod
    async def get_admin_by_id(admin_id:str) -> typing.Union[Admin, None]:

        query = Admin.objects(id=admin_id).first()

        return query
    

