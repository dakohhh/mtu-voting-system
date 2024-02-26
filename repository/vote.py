from bson import ObjectId
from database.schema import Student, Vote
from utils.query import VoteSchema


class VoteRepository:

    @staticmethod
    async def vote_for_candidate(student: Student, vote_input: VoteSchema) -> Vote:

        query = Vote(
            student=student,
            candidate=vote_input.candidate_id,
            election=vote_input.election_id,
        )

        query.save()

        return query

    @staticmethod
    async def has_voted_for_election(student: Student, election_id):

        query = Vote.objects(student=student, election=election_id).first()

        return query is not None

    @staticmethod
    async def get_election_results(election_id):

        pipeline = [
            {"$match": {"election": ObjectId(election_id)}},
            {"$group": {"_id": "$candidate", "count": {"$sum": 1}}},
        ]


        query = Vote.objects.aggregate(*pipeline)

        return query
