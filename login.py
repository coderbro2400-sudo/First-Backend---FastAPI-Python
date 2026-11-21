from fastapi import APIRouter, Depends, HTTPException
from db_pool import get_pool
from jwt_file import create_token, verify_token
from psycopg import Connection as Con
from pydantic import BaseModel
from rule import verify

class Login(BaseModel):
    email: str
    password: str


router = APIRouter()

@router.post("/login", status_code=200)
def login_users (data : Login,
                 conn: Con = Depends(get_pool)
                 ):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT id,name, password, role
        FROM users
        WHERE email = %s
        """, (data.email,)
                    )
        user = cur.fetchone()
        if user is None:
            raise HTTPException(
                    status_code=401,
                    detail="Username or Password wrong"
                    )
        is_correct = verify(data.password, user[2])
        if not is_correct:
            raise HTTPException(
                    status_code=401,
                    detail="Username or Password wrong"
                    )
        token = create_token(user[0],user[3])

        return {
                "msg": "Your login done",
                "user_id": user[0],
                "user_name": user[1],
                "user_role": user[3],

                "access_token": token,
                "token_type": "bearer",
                "Info": "please save this token and use carefully"
                }

