

from .database import Base
from sqlalchemy import Column,Integer,String,BOOLEAN,TIMESTAMP,ForeignKey,text,BigInteger
from sqlalchemy.orm import relationship



class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    is_published = Column(BOOLEAN,server_default = 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),server_default = text('now()'), nullable = False)
    owner_mailid = Column(String, ForeignKey("users.email",ondelete="CASCADE"),nullable = False) 

    owner = relationship("Users") 


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

class Comments(Base):
    __tablename__ = "comments"

    comment_id = Column(BigInteger, primary_key = True, nullable = False)
    posts_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    author_mail = Column(String,ForeignKey("users.email"))
    comments = Column(String, nullable = True)
    
class Follows(Base):
    __tablename__ = "follows"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),primary_key = True)
    follower_mail = Column(String, ForeignKey("users.email"),primary_key = True)



