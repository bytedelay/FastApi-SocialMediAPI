
from fastapi import HTTPException,status,APIRouter,Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from ..import models,utils,database,oauth2

router = APIRouter(tags=["Authentication"]) 


@router.post('/login') 
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    login_check = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    
    if not login_check:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"invalid Credentials")

    if not utils.verifyhash(user_credentials.password, login_check.password):  
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"invalid Credentials")

    access_token = oauth2.access_token_creation(data = {"username":user_credentials.username})
    
    return {"access_token":access_token,"token_type":"bearer"}

        