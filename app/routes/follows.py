
from ..import schemas,database,oauth2,models
from sqlalchemy.orm import Session
from fastapi import status, HTTPException,APIRouter,Depends

router = APIRouter(prefix = '/follows', tags=['Follow/UnFollow'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def followability(follow:schemas.Follows, db: Session = Depends(database.get_db), user_username:str=Depends(oauth2.get_current_user)):

    follow_check = db.query(models.Follows).filter(models.Follows.user_id == follow.user_id, 
        models.Follows.follower_mail == user_username.email)
    followed = follow_check.first()

    if (follow.dir==1):
        if followed:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f"The current user {user_username.email.split('@')[0]} has already followed the user {follow.user_id}")
            
        new_follow = models.Follows(user_id = follow.user_id, follower_mail = user_username.email)
        db.add(new_follow)
        db.commit()

        return {"message":f"The user {follow.user_id} has been followed"}

    else:
        
        if not followed:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        follow_check.delete(synchronize_session=False)
        db.commit()

        return {"message":f"You have unfollowed{user_username.email.split('@')[0]}"}
