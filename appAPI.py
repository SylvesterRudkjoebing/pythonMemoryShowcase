from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import dbObject
import bfsObject
import llmObject
from contextlib import asynccontextmanager

# Initialize database, BFS, and LLM
db = dbObject.MemoryDB()
bfs = bfsObject.bfsObject(db.conn)
llm = llmObject.llmObject()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the lifespan of the FastAPI application."""
    # Startup logic
    db.seedMemories()
    bfs.load_data("MemoryDB.db")
    llm.load_model()
    yield  # Application is running here
    # Shutdown logic
    db.close()

app = FastAPI(lifespan=lifespan)

# Allow cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Get the list of all people from the database
@app.get("/people/")
def get_people():
    """Fetch all people's names from the database."""
    people = db.get_all_people()
    if not people:
        raise HTTPException(status_code=404, detail="No people found.")
    return {"people": [person["name"] for person in people]}  # List of names

# Calculate memory associations
class RelationRequest(BaseModel):
    target_name: str

@app.post("/calculate-associations/")
def calculate_relations(request: RelationRequest):
    target_name = request.target_name

    try:
        associations = bfs.calculate(target_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    degrees = len(associations)
    return {"degrees": degrees, "associations": associations}

# Introduce LLM to provide context to the association
class LLMRequest(BaseModel):
    associations: list[str]

@app.post("/contextualize-associations/")
def contextualize_relations(request: LLMRequest):
    # prompt = "På 3 linjer, skriv disse vennehistorier: " + ", ".join(request.associations)
    prompt = ", ".join(request.associations)
    response = llm.communicate(prompt, max_tokens=5)
    return {"summary": response}
