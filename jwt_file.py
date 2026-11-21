from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials as HAC
from fastapi import Depends, HTTPException


S_KEY = "coder_bro_server"
ALGORITHM = "HS256"


#Create a Token generator
def create_token (user_id: int,
                  user_role: str):
    now = datetime.now(timezone.utc)
    payload = {
            "sub": str(user_id),
            "role": str(user_role),
            "exp": now + timedelta(minutes=30)
            }
    token = jwt.encode(payload,S_KEY,algorithm=ALGORITHM)
    
    return token

#collect tokem from reqest 
bearer_scheme = HTTPBearer()

#Create an Verify token generator
def verify_token (token: str):
    try:
        payload= jwt.decode(token, S_KEY, algorithms=[ALGORITHM],
                            options= {
                                "require": ["sub","exp"] }
                            )

        return payload
    except jwt.InvalidTokenError:
        return None

def define_user (credentials: HAC =Depends(bearer_scheme)
                 ):
    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
                status_code=401,
                detail="Invalid or expire token ",
                headers={ "WWW-Authenticate": "Bearer" }
                )
    return payload
