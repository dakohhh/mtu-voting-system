import threading
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, status
from authentication.auth import Auth
from database.schema import Admin, Student
from client.response import CustomResponse
from repository.admin import AdminRepository
from repository.candidate import CandidateRepository
from repository.department import DepartmentRepository
from repository.elections import ElectionRepository
from repository.vote import VoteRepository
from utils.query import (
    AdminSchema,
    CreateCandidateSchema,
    CreateElectionSchema,
    LoginSchema,
)
from exceptions.custom_exception import BadRequestException
from utils.task import save_candidate_image, save_election_image
from utils.upload import MTUVoteUpload, Upload


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

    return CustomResponse(
        "created admin user successfully", data=context, status=status.HTTP_201_CREATED
    )


@router.get("/election")
async def get_all_elections(
    request: Request, admin: Admin = Depends(auth.get_current_admin)
):

    elections = await ElectionRepository.get_all_elections(admin.department.id)

    context = {"elections": [election.to_dict() for election in elections]}

    return CustomResponse("get all elections", data=context)


@router.post("/election")
async def create_election(
    request: Request,
    election_name: str = Form(...),
    election_image: UploadFile = File(None),
    admin: Admin = Depends(auth.get_current_admin),
):
    election_input = CreateElectionSchema(election_name, election_image)

    election = await ElectionRepository.create_election(admin, election_input)

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


@router.get("/election/{id}")
async def get_all_candidates_for_election(
    request: Request,
    id: PydanticObjectId,
    admin: Admin = Depends(auth.get_current_admin),
):

    if not await ElectionRepository.does_election_exists(id):
        raise BadRequestException("this election doesn't exists")

    candidates = await CandidateRepository.get_all_candidate_on_election(id)

    context = {"candidates": [candidate.to_dict() for candidate in candidates]}

    return CustomResponse(
        "all candidates", data=context, status=status.HTTP_201_CREATED
    )


@router.post("/candidate")
async def add_candidate_to_election(
    request: Request,
    candidate_input: CreateCandidateSchema = Depends(),
    admin: Admin = Depends(auth.get_current_admin),
):

    if not await ElectionRepository.does_election_exists(candidate_input.election_id):

        raise BadRequestException("this election doesn't exists")

    candidate = await CandidateRepository.create_candidate(candidate_input)

    if candidate_input.candidate_image:

        if not candidate_input.candidate_image.content_type.startswith("image/"):
            raise BadRequestException("file sent is not a valid image")

        uploader = Upload("mtu_vote", str(candidate.id))

        upload_thread = threading.Thread(
            target=save_candidate_image,
            args=(
                candidate,
                uploader,
                candidate_input.candidate_image,
            ),
        )

        upload_thread.start()

    context = {"candidate": candidate.to_dict()}

    return CustomResponse(
        "created candidate successfully", data=context, status=status.HTTP_201_CREATED
    )


@router.delete("/candidate/{id}")
async def remove_candidate_from_election(
    request: Request,
    id: PydanticObjectId,
    admin: Admin = Depends(auth.get_current_admin),
):

    candidate = await CandidateRepository.get_candidate_by_id(id)

    if candidate is None:
        raise BadRequestException("this candidate doesn't exists")

    candidate.delete()

    return CustomResponse("deleted candidate successfully")


@router.delete("/election/{id}")
async def delete_election(
    request: Request,
    id: PydanticObjectId,
    admin: Admin = Depends(auth.get_current_admin),
):

    election = await ElectionRepository.get_election_by_id(id)

    if election is None:
        raise BadRequestException("this election doesn't exists")

    election.delete()

    return CustomResponse("deleted election successfully")


@router.get("/election/{id}/results")
async def get_election_results(
    request: Request,
    id: PydanticObjectId,
    admin: Admin = Depends(auth.get_current_admin),
):

    election_results = await VoteRepository.get_election_results(id)

    results = []

    for entry in election_results:

        candidate = await CandidateRepository.get_candidate_by_id(entry["_id"])

        candidate_dict = candidate.to_dict()

        candidate_dict.update({"vote_count": entry["count"]})

        results.append(candidate_dict)

    context = {"results": results}
    return CustomResponse("election voting results", data=context)
