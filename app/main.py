#from random import randrange


from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles


#from fastapi.params import Body
#import datetime
from . import models
from .database import  engine
from .routes import posts,users,auth,likes,dislikes
from .confg import settings  #used for encrypting values for protection 
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)


described = """
<h1>-----------------------------------------------------------------------------------------------------------------<img src="https://lh3.googleusercontent.com/McdS2RqVbNT2_JFjpTNQRXKFPebQ5GfzdtyuBAL7y2OoezBlSl-gttiq4qp16hvcaGqUVz2A3XMSF-mcDv5qJ9MDbecrlUscq3cYOhPhyoxoZwbgpFMFSLKWkUu3yymyBoneuwSzTA=w2400" alt="Logo" width="69" height="100"/></h1>

# Current Functionalities

## User Operations:

* **Create users**.
* **Read users**.
* **Read user by ID.**

## Posting related Operations:

* **Create new posts**
* **Read posts**
* **Update posts**
* **Delete posts**
* **Simultaneously Like and Dislike posts**
* **Likes Count**

## Features to be added:

* **Add Comments**
* **Follow/UnFollow Users**

<h1>-----------------------------------------------------------------------------------------------------------------</h1>

"""

app = FastAPI(title="ByteDelay's Social Media API",
    description=described,
    version="0.0.6")

#app.mount("/static", StaticFiles(directory="static"), name="static")

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
app.include_router(likes.router)
app.include_router(dislikes.router)


@app.get("/", tags=["Root"])   #used for name change in docs 
def root(): 
    return {"message": "Hail Hydra API"}





