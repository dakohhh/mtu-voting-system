import os
import certifi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect, errors
from routers.auth import router as auth
from routers.student import router as student
from exceptions.custom_exception import *
from dotenv import load_dotenv


load_dotenv()


CERTIFICATE = os.path.join(os.path.dirname(certifi.__file__), "cacert.pem")





if os.getenv("DEVELOPMENT"):
    connect(host=os.getenv("MONGODB_URL"))

else:
    connect(host=os.getenv("MONGODB_URL_ONLINE"), tls=True, tlsCAFile=CERTIFICATE)


app = FastAPI(title="MTU VOTING SYSTEM")





origins = [
    "http://127.0.0.1:5500/",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(student)
app.add_exception_handler(UserExistException, user_exist_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
app.add_exception_handler(ServerErrorException, server_exception_handler)
app.add_exception_handler(NotFoundException, not_found)
app.add_exception_handler(CredentialsException, credentail_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(errors.MongoEngineException, mongo_exception_handler)



