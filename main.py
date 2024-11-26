import dbObject
import bfsObject
import llmObject

def main(db, bfs, llm):
    # Seed the database with CSV data
    db.seedMemories()

    # Query example
    query_result = db.query('SELECT id FROM people')
    print(query_result)

    # Sets target friend name
    friend_name = "Jens"

    # Calculate how you met your friends
    relations = bfs.calculate(friend_name)

    # Close the SQLite database connection
    db.close()

    # Calculates and print reply based on input. Takes a very long time, since it's a local LLM, depending on your CPU/GPU.
    print(llm.communicate("På 3 linjer, fortæl historien omkring følgende møder: " + ", ".join(relations), 5))

if __name__ == "__main__":
    # Dependency Injection: Create instances of dependencies first
    db = dbObject.MemoryDB()  # Create the MemoryDB instance
    bfs = bfsObject.bfsObject(db.conn)  # Pass the database connection to BFS
    llm = llmObject.llmObject()  # Create the LLM object

    llm.load_model()  # Load the LLM model

    # Inject the created instances into the main function
    main(db, bfs, llm)
