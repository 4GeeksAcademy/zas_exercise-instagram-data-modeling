import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    userID = Column(Integer, primary_key=True)
    username = Column(String(50), index=True, nullable=False, unique=True)    # >-< DirectMessage.SenderID
    email = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    profilePicture = Column(String(50), nullable=False)
    createdAt = Column(DateTime)
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.

        #cascade="all, delete-orphan" incluye todas las opciones de cascada como borrar, actualizar etc... y elimina los hijos sin padres
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan") #(un usuario puede tener múltiples publicaciones).
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan") #(un usuario puede tener múltiples comentarios).
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan") #(un usuario puede dar múltiples "me gusta").
    followers = relationship("Follower", back_populates="followed", foreign_keys="[Follower.followedID]") # un usuario puede tener muchos seguidores
    following = relationship("Follower", back_populates="follower", foreign_keys="[Follower.followerID]") # un usuario puede seguir a muchos usuarios
    sent_messages = relationship("DirectMessage", back_populates="sender", foreign_keys="[DirectMessage.senderID]") # un usuario puede enviar muchos mensajes
    received_messages = relationship("DirectMessage", back_populates="receiver", foreign_keys="[DirectMessage.receiverID]") # un usuario puede recibir muchos mensajes

class Post(Base):
    __tablename__ = 'post'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    postID = Column(Integer, ForeignKey(User.userID), primary_key=True)
    userID = Column(Integer, ForeignKey(User.userID))
    image = Column(String(100), nullable=False)
    caption = Column(String(250))
    createdAt = Column(DateTime)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan") #un post puede tener múltiples comentarios
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan") #un post puede tener múltiples "likes"

class Comment(Base):
    __tablename__ = 'comment'
    commentID = Column(Integer, primary_key=True)
    postID = Column(Integer, ForeignKey(Post.postID), nullable=False)
    userID = Column(Integer, ForeignKey(User.userID), nullable=False)
    commentText = Column(Integer, ForeignKey(Post.postID), nullable=False)
    createdAt = Column(DateTime)

    user = relationship("User", back_populates="comments") # un comentario pertenece a un usuario
    post = relationship("Post", back_populates="comments") # un comentario pertenece a un post
                                                        # un usuario puede dejar varios comentarios en el mismo post

class Like (Base):
    __tablename__ = 'like'
    likeID = Column(Integer, primary_key=True)
    postID = Column(Integer, ForeignKey(Post.postID))
    userID = Column(Integer, ForeignKey(User.userID))
    createdAt = Column(DateTime)

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

class Follower(Base):
    __tablename__ = 'follower'
    followerID = Column(Integer, primary_key=True)
    followedID = Column(Integer, ForeignKey(User.userID))
    followerUserID = Column(Integer, ForeignKey(User.userID))
    followedAT = Column(DateTime)

    follower = relationship("User", back_populates="following", foreign_keys=[followerID]) #el usuario que sigue
    followed = relationship("User", back_populates="followers", foreign_keys=[followedID]) # el usuario seguido

class DirectMessage(Base):
    __tablename__ = 'directMessage'
    messageID = Column(Integer, primary_key=True)
    senderID = Column(Integer, ForeignKey(User.userID), nullable=False)
    receiverID = Column(Integer, ForeignKey(User.userID), nullable=False)
    messageText = Column(String(400), nullable=False)
    createdAt = Column(DateTime)

    sender = relationship("User", back_populates="sent_messages", foreign_keys=[senderID]) # el usuario que envía el mensaje
    receiver = relationship("User", back_populates="received_messages", foreign_keys=[receiverID]) # el usuario que recibe el mensaje

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e