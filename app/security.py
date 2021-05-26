import os
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status


X_API_KEY = APIKeyHeader(name='X-API-Key')
_API_KEY = os.getenv('API_KEY', '')

def check_authentication_header(x_api_key: str = Depends(X_API_KEY)):
    """ takes the X-API-Key header and converts it into the matching user object from the database """

    if x_api_key == _API_KEY:
        # Return True if key matched
        return True
    # else raise 401
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )
