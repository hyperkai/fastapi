from typing import List
from fastapi import FastAPI, Depends, responses, status, Response, HTTPException
from . import schema, model
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from .hashing import Hash

import blog

app = FastAPI()

model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    #if not blog.first():
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()

    return 'done'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schema.Blog, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return 'updated'

@app.get('/blog', response_model=List[schema.ShowBlog])
def all(db: Session = Depends(get_db)):
    blog = db.query(model.Blog).all()
    return blog

@app.get('/blog/{id}', status_code=200, response_model=schema.ShowBlog)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with the id {id} is not available")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'detail': f"Blog with the id {id} is not available"}
    return blog

@app.post('/user')
def create_user(request: schema.User, db: Session = Depends(get_db)):
    new_user = model.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
