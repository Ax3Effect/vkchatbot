import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    screen_name = Column(String(250))
    namecase = relationship("Namecases", uselist=False)

    is_blacklisted = Column(Integer, default=0)

    def getName(self):
        return "{} {}".format(self.first_name, self.last_name)

class Namecases(Base):
    __tablename__ = 'namecases'

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    nom = Column(String(250), nullable=False)
    gen = Column(String(250), nullable=False)
    dat = Column(String(250), nullable=False)
    acc = Column(String(250), nullable=False)
    ins = Column(String(250), nullable=False)
    abl = Column(String(250), nullable=False)

class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    chat_id = Column(Integer)
    timestamp = Column(Integer)
    message = Column(String)

 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.

if os.path.exists("sqlalchemy.db"):
    engine = create_engine('sqlite:///sqlalchemy.db', connect_args={'check_same_thread':False})
    Base.metadata.create_all(engine)
else:
    print("creating database...")
    engine = create_engine('sqlite:///sqlalchemy.db')
    Base.metadata.create_all(engine)

