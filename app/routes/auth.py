#Now for authentication

from fastapi import HTTPException,status,Response,APIRouter,Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from ..import models,schemas,utils,database,oauth2

router = APIRouter(tags=["Authentication"]) #current_tags = self.tags.copy() error refers to not putting tag in a list

'''
@router.post('/login')
def login(user_credentials:schemas.UserLogin, db: Session = Depends(database.get_db)):

    login_check = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()
    
    if not login_check:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"invalid Credentials")

    if not utils.verifyhash(user_credentials.password, login_check.password):  #storing this in a variable caused error 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"invalid Credentials")

    access_token = oauth2.access_token_creation(data = {"password":user_credentials.password}) #Scope of the data I am providing currently is "Id" so 

    
    return {"token":access_token,"token_type":"bearer token"}
'''

    

@router.post('/login') #issues on adding schema here schemas.Token
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    login_check = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    
    if not login_check:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"invalid Credentials")

    if not utils.verifyhash(user_credentials.password, login_check.password):  #storing this in a variable caused error 
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"invalid Credentials")

    access_token = oauth2.access_token_creation(data = {"username":user_credentials.username}) #Scope of the data I am providing currently is "Id" so 

    
    return {"access_token":access_token,"token_type":"bearer"}

        