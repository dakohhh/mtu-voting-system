from fastapi.responses import JSONResponse







class CustomResponse(JSONResponse):
    def __init__(self, messasge:str, status:int=200, success=True, data=None) -> None:

        response = {
        "status":status,
        "message": messasge,
        "success": success,
        "data": data 
        }

        super().__init__(status_code=status, content=response)



