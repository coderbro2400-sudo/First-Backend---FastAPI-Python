from jwt_file import define_user
from fastapi import Depends ,HTTPException
from db_pool import get_pool
from psycopg import Connection


def current_user (user: dict= Depends(define_user),
                  conn: Connection=Depends(get_pool)):
    user_id = int(user['sub'])
    with conn.cursor() as cur:
        cur.execute('''
        SELECT id, name, role
        FROM users
        WHERE id = %s
        ''',
                    (user_id,)
                    )
        info = cur.fetchone()

        if info is None:
            raise HTTPException(
                    status_code=401,
                    detail="Authentication Faild"
                    )
        return {
                'id': info[0],
                'name': info[1],
                'role': info[2]
                }

def require_role(*roles: str):
    def checker(user: dict= Depends(current_user)):
        role = user['role']
        if role not in roles:
            raise HTTPException(
                    status_code=403,
                    detail='Permission Denied'
                    )
        return user
    return checker
