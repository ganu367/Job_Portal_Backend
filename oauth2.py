from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = tokens.verify_token(data, credentials_exception)
    return token_data
