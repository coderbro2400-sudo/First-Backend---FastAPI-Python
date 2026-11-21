from pydantic import BaseModel, Field, EmailStr
from pwdlib import PasswordHash



pass_hash = PasswordHash.recommended()

def hasher (arg):
    hashed = pass_hash.hash(arg)
    return hashed


def verify (password, hashed):
    is_correct = pass_hash.verify(password, hashed)
    return is_correct

class Create (BaseModel):
    name : str = Field (min_length=3, max_length=50)
    email : EmailStr
    password : str = Field (min_length=8,max_length=20)

class Login (BaseModel):
    email : EmailStr
    password : str
