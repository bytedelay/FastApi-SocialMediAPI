#from random import randrange

from fastapi import FastAPI
#from fastapi.params import Body
#import datetime

from . import models
from .database import  engine
from .routes import posts,users,auth
from .confg import settings  #used for encrypting values for protection 
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

#origins = ["https://www.google.com"] #Cross-Origin Resource Sharing # to be restrictive
origins = ["*"]  #for all websites 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", tags=["Root"])   #used for name change in docs 
def root(): 
    return {"message": "Hail Hydra API"} 
