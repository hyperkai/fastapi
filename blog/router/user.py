from fastapi import APIRouter, Depends
from .. import database, schema
from sqlalchemy.orm import Session
from ..repository import user

router = APIRouter(
    prefix='/user',
    tags=['User']
)

get_db = database.get_db

@router.post('/', response_model=schema.ShowUser)
def create_user(request: schema.User, db: Session = Depends(get_db)):
    return user.create(request, db)

@router.get('/{id}', status_code=200, response_model=schema.ShowUser)
def get_user(id:int, db: Session = Depends(get_db)):
    return user.show(id, db)