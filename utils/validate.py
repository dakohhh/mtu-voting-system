from bson import ObjectId
from exceptions.custom_exception import BadRequestException




def get_object_id(id:str):
    try:
        return ObjectId(id)
    
    except:
        raise BadRequestException(f"{id} is not a valid object id")
    
