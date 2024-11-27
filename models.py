# models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    birth = Column(String)
    
    # Relationship to the events through participations
    events = relationship("Participation", back_populates="person")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True)
    event = Column(String)
    year = Column(Integer)
    
    # Relationship to people through participations
    participations = relationship("Participation", back_populates="event")

class Participation(Base):
    __tablename__ = "participations"
    
    person_id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), primary_key=True)
    
    person = relationship("Person", back_populates="events")
    event = relationship("Event", back_populates="participations")
