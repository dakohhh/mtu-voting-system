import threading
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, status
from authentication.auth import Auth
from database.schema import Admin, Student
from client.response import CustomResponse
from repository.admin import AdminRepository
from repository.department import DepartmentRepository
from repository.elections import ElectionRepository
from utils.query import AdminSchema, CreateElectionSchema, LoginSchema
from exceptions.custom_exception import BadRequestException
from utils.task import save_election_image
from utils.upload import MTUVoteUpload


router = APIRouter(tags=["Admin"], prefix="/admin")


auth = Auth()


@router.post("/create")
async def create_admin(request: Request, secret: str, admin_input: AdminSchema):

    if secret != "wisdom12":
        raise BadRequestException("incorrect secret")

    if await AdminRepository.does_admin_exist(admin_input.email):

        raise BadRequestException("The email already exists")

    admin = await AdminRepository.create_admin(admin_input)

    context = {"admin": admin.to_dict()}

    return CustomResponse("login user successfully", data=context)


@router.post("/election")
async def create_election(
    request: Request,
    department_id: PydanticObjectId = Form(...),
    election_name: str = Form(...),
    election_image: UploadFile = File(None),
):
    election_input = CreateElectionSchema(department_id, election_name, election_image)

    print(election_input.election_image)

    if not await DepartmentRepository.does_department_exist(
        election_input.department_id
    ):
        raise BadRequestException("this department doesn't exist")

    election = await ElectionRepository.create_election(election_input)

    if election_input.election_image:

        if not election_input.election_image.content_type.startswith("image/"):
            raise BadRequestException("file sent is not a valid image")

        uploader = MTUVoteUpload(str(election.id))

        upload_thread = threading.Thread(
            target=save_election_image,
            args=(
                election,
                uploader,
                election_input.election_image,
            ),
        )


        upload_thread.start()


    context = {"election": election.to_dict()}

    return CustomResponse("created election successfully", data=context)





@router.delete("/election/{id}")
async def remove_election(
    request: Request, admin: Admin = Depends(auth.get_current_admin)
):

    context = {"admin": admin.to_dict()}

    return CustomResponse("login user successfully", data=context)
