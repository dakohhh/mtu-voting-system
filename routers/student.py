import asyncio
from beanie import PydanticObjectId
from pydantic import EmailStr
from fastapi import APIRouter, Depends, Request, BackgroundTasks, status
from authentication.auth import Auth
from authentication.hashing import checkPassword, hashPassword
from client.response import CustomResponse
from database.schema import Student
from repository.candidate import CandidateRepository
from repository.department import DepartmentRepository
from repository.elections import ElectionRepository
from repository.otp import OTPRespository
from repository.student import StudentRepository
from repository.vote import VoteRepository
from utils.func import generate_random_otp
from utils.query import SignupSchema, VoteSchema
from exceptions.custom_exception import BadRequestException
from utils.task import send_otp_mail


router = APIRouter(tags=["Student"], prefix="/student")


auth = Auth()


@router.post("/signup")
async def signup_student(request: Request,background_task: BackgroundTasks,  signup_input: SignupSchema):

    tasks = [
        StudentRepository.does_student_email_exits(signup_input.email),
        DepartmentRepository.does_department_exist(signup_input.department_id),
    ]

    (
        email_exits,
        department_exist,
    ) = await asyncio.gather(*tasks)

    if email_exits:

        raise BadRequestException("email already exists")

    if not department_exist:

        raise BadRequestException("department does not exists")

    student = await StudentRepository.create_student(signup_input)

    otp = generate_random_otp()

    if await OTPRespository.does_otp_exist(student):

        await OTPRespository.update_otp(student, hashPassword(str(otp)))

    else:
        await OTPRespository.create_otp(student, hashPassword(str(otp)))

    background_task.add_task(send_otp_mail, student, otp)

    context = {"student": student.to_dict()}

    return CustomResponse(
        "signup student successfully, please verify your email", data=context, status=status.HTTP_201_CREATED
    )


# @router.post("/send_voting_number")
# async def send_voting_number(
#     request: Request, student: Student = Depends(auth.get_current_student)
# ):

#     context = {"student": student.to_dict()}

#     return CustomResponse("signup student successfully", data=context)


# @router.post("/request_otp")
# async def request_otp(
#     request: Request, email: EmailStr, background_task: BackgroundTasks
# ):

#     student = await StudentRepository.get_student_by_email(email)

#     if student is None:
#         raise BadRequestException("this email doesn't exists")

#     otp = generate_random_otp()

#     if await OTPRespository.does_otp_exist(student):

#         await OTPRespository.update_otp(student, hashPassword(str(otp)))

#     else:
#         await OTPRespository.create_otp(student, hashPassword(str(otp)))

#     background_task.add_task(send_otp_mail, student, otp)

#     return CustomResponse("sent otp successfully", data={"otp": str(otp)})


@router.post("/verify")
async def verify_student(request: Request, email: EmailStr, otp: str):

    student = await StudentRepository.get_student_by_email(email)

    if student is None:
        raise BadRequestException("this email doesn't exists")

    hash_otp = await OTPRespository.get_otp(student)

    if hash_otp is None or not checkPassword(otp, hash_otp.otp):
        raise BadRequestException("Invalid OTP")

    student.is_verified = True

    student.save()

    hash_otp.delete()

    context = {"student": student.to_dict()}

    return CustomResponse("student verified successfully", data=context)


@router.get("/election")
async def get_all_elections(
    request: Request, student: Student = Depends(auth.get_current_student)
):

    elections = await ElectionRepository.get_all_elections(student.department)

    context = {"elections": [election.to_dict() for election in elections]}

    return CustomResponse("get elections for student", data=context)


@router.get("/election/{id}")
async def get_candidates_on_elections(
    request: Request,
    id: PydanticObjectId,
    student: Student = Depends(auth.get_current_student),
):

    if not await ElectionRepository.does_election_exists(id):

        raise BadRequestException("this election doesn't exists")

    candidates = await CandidateRepository.get_all_candidate_on_election(id)

    context = {"candidates": [candidate.to_dict() for candidate in candidates]}

    return CustomResponse("get candidates for election", data=context)


@router.post("/election/vote")
async def vote_for_candidate(
    request: Request,
    vote_input: VoteSchema,
    student: Student = Depends(auth.get_current_student),
):
    tasks = [
        ElectionRepository.does_election_exists(vote_input.election_id),
        CandidateRepository.does_candidate_exist(vote_input.candidate_id),
    ]

    (
        election_exists,
        candidate_exists,
    ) = await asyncio.gather(*tasks)

    

    if not election_exists:
        raise BadRequestException("this election doesn't exists")
    

    if not candidate_exists:
        raise BadRequestException("this candidate doesn't exists")
    
    
    if await VoteRepository.has_voted_for_election(student, vote_input.election_id):
        raise BadRequestException("you have voted on this election already!")
    

    vote = await VoteRepository.vote_for_candidate(student, vote_input)


    return CustomResponse("vote for candidate successfuly", data=None)

    