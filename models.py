from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.schema import MetaData

# Use a naming convention for constraints to help with migrations
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

# Create a base class for declarative models
Base = declarative_base(metadata=metadata)

# Association table for many-to-many relationship between people and events
participations = Table('participations', Base.metadata,
    Column('person_id', Integer, ForeignKey('people.id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True)
)

class Person(Base):
    """
    Represents a person in the database.
    """
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth = Column(Integer)

    # Many-to-many relationship with events
    events = relationship(
        "Event", 
        secondary=participations, 
        back_populates="participants"
    )

    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}', birth='{self.birth}')>"

class Event(Base):
    """
    Represents an event in the database.
    """
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    event = Column(String, nullable=False)
    year = Column(Integer)

    # Many-to-many relationship with people
    participants = relationship(
        "Person", 
        secondary=participations, 
        back_populates="events"
    )

    def __repr__(self):
        return f"<Event(id={self.id}, event='{self.event}', year='{self.year}')>"

class DatabaseManager:
    """
    Manages database connections and sessions using SQLAlchemy.
    """
    def __init__(self, database_url='sqlite:///MemoryDB.db'):
        """
        Initialize the database engine and session factory.
        
        :param database_url: SQLAlchemy database URL
        """
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        """
        Create all tables defined in the models.
        """
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """
        Create a new database session.
        
        :return: SQLAlchemy session
        """
        return self.SessionLocal()

    def close(self):
        """
        Close the database engine.
        """
        self.engine.dispose()

# Example usage function
def example_usage():
    # Initialize the database manager
    db_manager = DatabaseManager()

    # Create tables if they don't exist
    db_manager.create_tables()

    # Create a session
    session = db_manager.get_session()

    try:
        # Example: Add a new person
        new_person = Person(name="John Doe", birth="1990-01-01")
        session.add(new_person)

        # Example: Add a new event
        new_event = Event(event="Meeting", year="2023")
        session.add(new_event)

        # Example: Create a relationship
        new_person.events.append(new_event)

        # Commit the transaction
        session.commit()

        # Query examples
        # Find all people
        all_people = session.query(Person).all()
        print("All People:", all_people)

        # Find events for a specific person
        person = session.query(Person).filter_by(name="John Doe").first()
        if person:
            print(f"Events for {person.name}:", person.events)

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

    finally:
        # Close the session
        session.close()

if __name__ == "__main__":
    example_usage()