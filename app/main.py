
from fastapi import FastAPI

from . import models
from .database import  engine
from .routes import posts,users,auth,likes,dislikes,comments,follows
from .confg import settings  
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
* **Added Follow/unFollow Users**
* **Added Comments**

## Features to be added:

* **Comments Deletion Option**
* **Comments returned as list of comments for user**

<h1>-----------------------------------------------------------------------------------------------------------------</h1>

"""

app = FastAPI(title="ByteDelay's Social Media API",
    description=described,
    version="0.0.7")

origins = ["*"]  

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
app.include_router(comments.router)
app.include_router(follows.router)


@app.get("/", tags=["Root"])   
def root(): 
    return {"message": "Hail Hydra API"}





