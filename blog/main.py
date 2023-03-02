from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import *
import models , schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Creating a Blog Post
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# To List All blog posts
@app.get('/blog')
def all(db: Session = Depends(get_db)):
     blogs = db.query(models.Blog).all()
     return blogs

# To get specified id Blog details
@app.get('/blog/{id}', status_code=200)
def show(id, responce: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} is not available')
        # responce.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with the id {id} is not available'}
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def updated(id, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update({'title': 'updated title'},synchronize_session=False)
    return 'Updated Successfully'