from fastapi import FastAPI ,Request
from psycopg_pool import ConnectionPool
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()
@asynccontextmanager
async def lifespan (app: FastAPI):
    pool = ConnectionPool(
            conninfo= os.environ["DB_URL"],
            min_size=1,
            max_size=5,
            open=False
            )
    pool.open()
    app.state.pool = pool

    try :
        yield
    finally:
        pool.close()

app = FastAPI(lifespan=lifespan)

def get_pool(req: Request):
    with req.app.state.pool.connection() as conn:
        yield conn
