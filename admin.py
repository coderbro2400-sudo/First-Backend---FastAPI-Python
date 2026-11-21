from fastapi import APIRouter, Depends, HTTPException
from psycopg import Connection
from db_pool import get_pool
from role import current_user, require_role

router = APIRouter()

@router.get('/admin', status_code=200)
def admin_area (admin: dict = Depends(require_role('sudo','admin')),
                conn: Connection = Depends(get_pool)
                ):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT id,name,role
        FROM users
        ''')
        alls = cur.fetchall()
        msg = f"Wealcome here {admin['role']} :- {admin['name']}, Developer MR. R (WD)"

        
        return [
                {
                    'intro': msg,
                    '--': "=====",
                    'id': row[0],
                    'name': row[1],
                    'role': row[2]
                    }
                for row in alls
                ]

