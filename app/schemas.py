from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional



class POSTBase(BaseModel):  #class POST extending imported BaseModel from pydantic
    title:str
    content:str
    #adding new methods
    is_published:bool = True #default true
    #owner: RespondUser  #pydantic data form


#These two controls what client sends or requests
class POSTCreate(POSTBase): #Inheritance
    pass 

class UserCreate(BaseModel): #for creating user schema
    email:EmailStr
    password:str

class UserLogin(BaseModel):

    email:EmailStr
    password:str

class Token(BaseModel):

    access_token:str
    token_type:str

class TokenData(BaseModel):
    #id: int
    email: Optional[str]

#Response control #This dictates what we send as a response for client stuff
class RespondUser(BaseModel):
    id:int
    email:EmailStr
    #password:str
    created_at:datetime

    class Config:
        orm_mode = True   #Moved RespondUser up cos it wasn't declared yet.
        
class Respond(POSTBase): #Inheriting to avoid re-structuring and with this we have more control.#issues with that
    id:int    
    created_at:datetime
    #email: Optional[str]
    owner_mailid:str
    owner: RespondUser

    class Config:
        orm_mode = True #this skips the error as pydantic model understands it's a sqlalchemy


#Looks similar but as a repsonse we also got hidden parameters earlier now we would be skipping that.

class Like(BaseModel):
    posts_id : int
    dir: conint(ge=0,le=1) #used for setting value between 0 and 1.

class DisLike(BaseModel):
    posts_id : int
    dir: conint(ge=0,le=1) #used for setting value between 0 and 1.



