from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings

from adapters import SMS, Email

limiter = Limiter(key_func=get_remote_address)

def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.state.limiter = limiter
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

sms = SMS()
email = Email()


@app.post("/send_sms")
@limiter.limit("5/minute")
def send_sms(destination: str, message: str, request: Request):
    message_payload = {}
    return sms.send(destination, message)


@app.post("/send_email")
@limiter.limit("5/minute")
def send_sms(recipient: str, subject: str, message: str, request: Request):
    message_payload = {}
    return email.send([recipient], subject, message)