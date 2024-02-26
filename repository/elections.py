from database.schema import Election
from utils.query import CreateElectionSchema


class ElectionRepository:

    @staticmethod
    async def create_election(election_input: CreateElectionSchema) -> Election:

        default_image = "https://res.cloudinary.com/do1iufmkf/image/upload/v1708865355/mtu_vote/nvkutk9ybtl4xs7ikf6g.png"

        query = Election(
            election_name=election_input.election_name,
            department=election_input.department_id,
            election_image=default_image,
        )

        query.save()

        return query

    @staticmethod
    async def get_all_elections(department_id):

        query = Election.objects(department=department_id).all()

        return query

    @staticmethod
    async def does_election_exists(election_id):

        query = Election.objects(id=election_id).first()

        return query is not None
    

    @staticmethod
    async def get_election_by_id(election_id) -> Election:

        query = Election.objects(id=election_id).first()

        return query
