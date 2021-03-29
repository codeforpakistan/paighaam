from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings

# our own imports
from adapters import SMS, Email

# define the slow-api limiter
limiter = Limiter(key_func=get_remote_address)

# convenient function to bootstrap the FastAPI object
def get_application():

    tags_metadata = [
        {
            "name": "sms",
            "description": "Send a omni-channel SMS.",
        },
        {
            "name": "email",
            "description": "Semd a omni-channel Email.",
        },
    ]

    _app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Allows government departments to communicate with the citizens through a unified omni-channel communication gateway.",
        version="v0.0.1",
        openapi_tags=tags_metadata,
    )

    # setting the limiter here
    _app.state.limiter = limiter

    # add graceful exception handling in case ratelimit exceeeds
    _app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

# create objects to use via adapters namespace
sms = SMS()
email = Email()


@app.post("/sms", tags=['sms'])
@limiter.limit("5/minute")
def send_sms(destination: str, message: str, request: Request):
    message_payload = {}
    return sms.send(destination, message)


@app.post("/email", tags=['email'])
@limiter.limit("5/minute")
def send_sms(recipient: str, subject: str, message: str, request: Request):
    message_payload = {}
    return email.send([recipient], subject, message)
