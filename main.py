from fastapi import Depends
from db_pool import app
from user import router as user_router
from admin import router as admin_router
from login import router as log_router

app.include_router(user_router)
app.include_router(admin_router)
app.include_router(log_router)
