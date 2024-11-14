import sys
import dbObject
import bfsObject
import llmObject

def main():
    # Create an instance of MemoryDB with a database file
    db = dbObject.MemoryDB()

    # Seed the database with CSV data
    db.seedMemories()   

    # Query example
    query_result = db.query('SELECT name FROM people')
    print(query_result)

    # Creates BFS object
    bfs = bfsObject.bfsObject(db.conn)

    # Sets source and target name
    target_name = input("Name: ")

    # Calculate how you met your friends
    bfs.calculate(target_name)

    # Close the SQLite database connection
    db.close()

    # Creates and loads the Llama Object (Llama-3.2-1B)
    llm = llmObject.llmObject()
    llm.load_model()

    # Calculates and print reply based on input. Takes a very long time, since it's a local llm, depending on your CPU/GPU.
    print(llm.communicate("How many fingers are on 2 hands?", 20))

if __name__ == "__main__":
    main()
