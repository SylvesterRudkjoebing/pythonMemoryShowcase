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

    # Sets target friend name
    # friend_name = input("Name: ")
    friend_name = "Den introverte Assembly-programmør"

    # Calculate how you met your friends
    relations = bfs.calculate(friend_name)

    # Close the SQLite database connection
    db.close()

    # Creates and loads the Llama Object (Llama-3.2-1B)
    llm = llmObject.llmObject()
    llm.load_model()

    # Calculates and print reply based on input. Takes a very long time, since it's a local llm, depending on your CPU/GPU.
    print(llm.communicate("På 3 linjer, fortæl historien omkring følgende møder: " + ", ".join(relations), 5))

if __name__ == "__main__":
    main()
