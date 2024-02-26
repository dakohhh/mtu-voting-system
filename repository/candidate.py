from beanie import PydanticObjectId
from fastapi import Query
from database.schema import Candidate
from utils.query import CreateCandidateSchema


class CandidateRepository:

    @staticmethod
    async def create_candidate(candidate_input: CreateCandidateSchema):

        default_image = "https://res.cloudinary.com/do1iufmkf/image/upload/v1708870941/mtu_vote/i1prdyd7bnif71wbbbn5.png"

        query = Candidate(
            candidate_name=candidate_input.candidate_name,
            candidate_image=default_image,
            election=candidate_input.election_id,
        )

        query.save()

        return query

    @staticmethod
    async def get_all_candidate_on_election(election_id):

        query = Candidate.objects(election=election_id).all()

        return query

    @staticmethod
    async def does_candidate_exist(candidate_id):

        query = Candidate.objects(id=candidate_id).first()

        return query is not None

    @staticmethod
    async def get_candidate_by_id(candidate_id) -> Candidate:

        query = Candidate.objects(id=candidate_id).first()

        return query
