import pandas as pd
from models import DatabaseManager, Person, Event, participations

class MemoryDB:
    def __init__(self, db_filename="memoryDB.db"):
        """
        Initialize SQLAlchemy database connection.
        
        :param db_filename: Name of the SQLite database file
        """
        database_url = f'sqlite:///{db_filename}'
        self.db_manager = DatabaseManager(database_url)
        self.conn = self.db_manager.engine.connect()
        print(f"Connected to SQLite database '{db_filename}'.")

    def load_csv(self, file_path):
        """
        Loads a CSV file into a Pandas DataFrame.
        
        :param file_path: Path to the CSV file
        :return: Pandas DataFrame
        """
        return pd.read_csv(file_path)

    def insert_dataframe(self, df, table_name, if_exists='replace'):
            """
            Inserts a DataFrame into a SQLite table using SQLAlchemy.
            
            :param df: DataFrame to insert
            :param table_name: Name of the target table
            :param if_exists: Behavior when the table exists ('fail', 'replace', 'append')
            """
            session = self.db_manager.get_session()
            try:
                # Clear existing data if replacing
                if if_exists == 'replace':
                    if table_name == 'people':
                        session.query(Person).delete()
                    elif table_name == 'events':
                        session.query(Event).delete()
                
                # Insert new data
                for _, row in df.iterrows():
                    if table_name == 'people':
                        person = Person(id=row['id'], name=row['name'], birth=row['birth'])
                        session.add(person)
                    elif table_name == 'events':
                        event = Event(id=row['id'], event=row['event'], year=row['year'])
                        session.add(event)
                
                session.commit()
                print(f"Data inserted into table '{table_name}' successfully.")
            except Exception as e:
                session.rollback()
                print(f"Error inserting data: {e}")
            finally:
                session.close()

    def seedMemories(self):
        self.db_manager.create_tables()

        session = self.db_manager.get_session()
        try:
            people_count = session.query(Person).count()
            events_count = session.query(Event).count()
            participation_count = session.query(participations).count()  # Add this line

            if people_count == 0 and events_count == 0 and participation_count == 0:
                file_paths = ['data/small/events.csv', 'data/small/people.csv', 'data/small/participations.csv']

                for file_path in file_paths:
                    table_name = file_path.split('/')[-1].replace('.csv', '')
                    df = self.load_csv(file_path)
                    
                    if table_name == 'participations':
                        # Add code to insert participations
                        for _, row in df.iterrows():
                            stmt = participations.insert().values(
                                person_id=int(row['person_id']), 
                                event_id=int(row['event_id'])
                            )
                            session.execute(stmt)
                    else:
                        self.insert_dataframe(df, table_name)
                
                session.commit()
                print("Seeding completed.")
            else:
                print("Database already contains data. Skipping seeding.")
        except Exception as e:
            session.rollback()
            print(f"Error seeding database: {e}")
        finally:
            session.close()

    def get_all_people(self):
        """
        Fetch all people's names using SQLAlchemy.
        
        :return: List of names from the people table
        """
        session = self.db_manager.get_session()
        try:
            people = session.query(Person).all()
            return [{"name": person.name} for person in people]
        finally:
            session.close()

    def create_person(self, id, name, birth):
        """
        Adds a new person to the database using SQLAlchemy.
        """
        session = self.db_manager.get_session()
        try:
            person = Person(id=id, name=name, birth=birth)
            session.add(person)
            session.commit()
            print(f"Added person: {id} {name} ({birth})")
        except Exception as e:
            session.rollback()
            print(f"Error adding person: {e}")
        finally:
            session.close()

    def get_person(self, person_id):
        """
        Fetches a person's details by ID using SQLAlchemy.
        """
        session = self.db_manager.get_session()
        try:
            person = session.query(Person).filter(Person.id == person_id).first()
            if person:
                return {"id": person.id, "name": person.name, "birth": person.birth}
            return None
        finally:
            session.close()

    def update_person(self, person_id, name=None, birth=None):
        """
        Updates a person's details in the database using SQLAlchemy.
        """
        session = self.db_manager.get_session()
        try:
            person = session.query(Person).filter(Person.id == person_id).first()
            if person:
                if name:
                    person.name = name
                if birth:
                    person.birth = birth
                session.commit()
                print(f"Updated person with ID: {person_id}")
            else:
                print(f"No person found with ID: {person_id}")
        except Exception as e:
            session.rollback()
            print(f"Error updating person: {e}")
        finally:
            session.close()

    def delete_person(self, person_id):
        """
        Deletes a person from the database using SQLAlchemy.
        """
        session = self.db_manager.get_session()
        try:
            person = session.query(Person).filter(Person.id == person_id).first()
            if person:
                session.delete(person)
                session.commit()
                print(f"Deleted person with ID: {person_id}")
            else:
                print(f"No person found with ID: {person_id}")
        except Exception as e:
            session.rollback()
            print(f"Error deleting person: {e}")
        finally:
            session.close()

    def query(self, query):
        """
        Executes a SQL query and returns the results as a DataFrame.
        
        :param query: SQL query string
        :return: DataFrame containing query results
        """
        return pd.read_sql(query, self.conn)

    def close(self):
        """Closes the connection to the SQLite database."""
        self.conn.close()
        self.db_manager.close()
        print(f"Connection to database closed.")


    def inspect_participations(self):
        session = self.db_manager.get_session()
        try:
            # Get a few sample participations
            parts = session.query(participations).limit(10).all()
            print("Sample Participations:")
            for part in parts:
                print(f"Person ID: {part.person_id}, Event ID: {part.event_id}")

            # Count total participations
            count = session.query(participations).count()
            print(f"\nTotal Participations: {count}")

        finally:
            session.close()