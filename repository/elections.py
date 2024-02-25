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
