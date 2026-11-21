from fastapi import APIRouter, HTTPException, Depends
from role import current_user
from psycopg import Connection
from db_pool import get_pool


router = APIRouter()

@router.get('/users/id/{user_id}',status_code=200)
def find_user( user_id: int,
              user: dict = Depends(current_user)
              ):
    if user_id != user['id']:
        raise HTTPException(
                status_code=403,
                detail='Not Allowed'
                )
    return user

@router.get('/users/all', status_code=200)
def show_all (conn: Connection = Depends (get_pool),
              user: dict = Depends(current_user)
              ):
    with conn.cursor() as cur:
        cur.execute( '''
        SELECT id, name, role
        FROM users
        LIMIT 10
        ''')
        user_list = cur.fetchall()

        return [
                {
                'id': row[0],
                'name': row[1],
                'role': row[2]
                }
                for row in user_list
                ]
