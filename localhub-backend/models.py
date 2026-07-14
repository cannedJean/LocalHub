from datetime import datetime
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), unique=True, index=True, nullable=False)
    name = Column(String(128), nullable=False)

    posts = relationship("Post", back_populates="region")
    festivals = relationship("Festival", back_populates="region")
    attractions = relationship("Attraction", back_populates="region")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    title = Column(String(250), nullable=False)
    content = Column(Text, nullable=False)
    author_name = Column(String(100), nullable=True, default="익명")
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    region = relationship("Region", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    view_count = Column(Integer, default=0)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_name = Column(String(100), nullable=True, default="익명")
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="comments")


class Festival(Base):
    __tablename__ = "festivals"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    title = Column(String(250), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    location = Column(String(250), nullable=True)

    region = relationship("Region", back_populates="festivals")


class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    name = Column(String(250), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    region = relationship("Region", back_populates="attractions")
