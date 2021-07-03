from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import model, schema
from ..hashing import Hash


def create(request: schema.User, db: Session):
    new_user = model.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with the id {id} is not available")
    return user