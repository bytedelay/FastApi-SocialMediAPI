

from .database import Base
from sqlalchemy import Column,Integer,String,BOOLEAN,TIMESTAMP,ForeignKey,text
from sqlalchemy.orm import relationship


#works only when no table with said name is present.
#Database Table Creation

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    is_published = Column(BOOLEAN,server_default = 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),server_default = text('now()'), nullable = False)
    owner_mailid = Column(String, ForeignKey("users.email",ondelete="CASCADE"),nullable = False) #"database_name.id = users.id"

    owner = relationship("Users") #making a relationship so that we can access both


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),server_default = text('now()'), nullable = False)


class Likes(Base):
    __tablename__ = "likes"

    posts_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),primary_key = True)
    author_mail = Column(String, ForeignKey("users.email"),primary_key = True)

class DisLikes(Base):
    __tablename__ = "dislikes"

    posts_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),primary_key = True)
    author_mail = Column(String, ForeignKey("users.email"),primary_key = True)