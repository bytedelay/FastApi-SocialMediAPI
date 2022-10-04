
from ..import schemas,database,oauth2,models,database
from sqlalchemy.orm import Session
from fastapi import status, HTTPException,APIRouter,Depends


router = APIRouter(prefix = '/dislike', tags=['DISLIKE'])
#do not keep "filename.py" and functionname.py same

@router.post("/", status_code=status.HTTP_201_CREATED)
def dislikeness(vote:schemas.DisLike, db: Session = Depends(database.get_db), user_username:str=Depends(oauth2.get_current_user)):
    
    post_presence = db.query(models.DisLikes).filter(models.Post.id == vote.posts_id).first()

    if not post_presence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    dislike_check = db.query(models.DisLikes).filter(models.DisLikes.posts_id == vote.posts_id, 
        models.DisLikes.author_mail == user_username.email)#checking if already voted.#Second condition mail check
    disliked = dislike_check.first()
    
    if (vote.dir==1):
        if disliked:
            #print(user_username.email.split('@')[0])
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f"The current user {user_username.email.split('@')[0]} has already disliked the post {vote.posts_id}")
            
        new_dislike = models.DisLikes(posts_id = vote.posts_id, author_mail = user_username.email)
        db.add(new_dislike)
        db.commit()
        return {"message":f"The Post {vote.posts_id} has been disliked"}

    else:

        if not disliked:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        dislike_check.delete(synchronize_session=False)
        db.commit()
        return {"message":f"You have withdrawn your dislike{user_username.email.split('@')[0]}"}
