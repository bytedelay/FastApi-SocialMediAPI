
from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional

class POSTBase(BaseModel):
    title:str
    content:str
    is_published:bool = True

class POSTCreate(POSTBase):
    pass 

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email: Optional[str]

class RespondUser(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True  
        
class Respond(POSTBase): 
    id:int    
    created_at:datetime
    owner_mailid:str
    owner: RespondUser

    class Config:
        orm_mode = True 

class LikesDisplay(BaseModel): 
    Post:Respond
    no_of_likes:int

    class Config:
        orm_mode = True


class Like(BaseModel):
    posts_id : int
    dir: conint(ge=0,le=1) 

class DisLike(BaseModel):
    posts_id : int
    dir: conint(ge=0,le=1) 

class Comments(BaseModel):
    posts_id : int
    comments : str

class Follows(BaseModel):
    user_id : int
    dir: conint(ge=0, le=1)





