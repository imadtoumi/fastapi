from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey


# This model repsents a tables which is the posts table
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content= Column(String, nullable=False)
    published= Column(Boolean, server_default='True', nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey(column="users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User")

class User(Base):
    __tablename__ = "users"

    id= Column(Integer, primary_key=True, nullable=False)
    email= Column(String, nullable=False, unique=True)
    password= Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))