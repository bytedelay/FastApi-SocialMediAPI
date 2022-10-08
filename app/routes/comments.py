
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter,status,HTTPException,Depends

router = APIRouter(prefix = '/comments', tags=['Comment'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def commentar(comment:schemas.Comments, db:Session = Depends(database.get_db), user_username:str=Depends(oauth2.get_current_user)):

    post_presence = db.query(models.Comments).filter(models.Post.id == comment.posts_id).first()

    if not post_presence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    new_comment = models.Comments(author_mail = user_username.email,**comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {"message":f"Your comment '{new_comment.comments}' has been submitted with comment id {new_comment.comment_id}"}


