from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
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
    allow_origins=["http://localhost:3000", "http://frontend:3000"],  # Allow frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Add a route for the root ("/") to redirect to "/people/"
@app.get("/")
def redirect_root():
    return RedirectResponse(url="/people/")

# Get the list of all people from the database
@app.get("/people/")
def get_people():
    """Fetch all people's names from the database."""
    people = db.get_all_people()
    if not people:
        raise HTTPException(status_code=404, detail="No people found.")
    return {"people": [person["name"] for person in people]}  # List of names

class PersonCreateRequest(BaseModel):
    id: int
    name: str
    birth: str

@app.post("/people/")
def add_person(person: PersonCreateRequest):
    try:
        db.create_person(person.id, person.name, person.birth)
        return {"message": "Person added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/people/{person_id}")
def read_person(person_id: int):
    person = db.get_person(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@app.put("/people/{person_id}")
def update_person(person_id: int, name: str = None, birth: str = None):
    try:
        db.update_person(person_id, name, birth)
        return {"message": "Person updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/people/{person_id}")
def delete_person(person_id: int):
    try:
        db.delete_person(person_id)
        return {"message": "Person deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

class EventCreateRequest(BaseModel):
    id: int
    event: str
    year: int

@app.post("/events/")
def add_event(event: EventCreateRequest):
    try:
        db.create_event(event.id, event.event, event.year)
        return {"message": "Event added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ParticipationCreateRequest(BaseModel):
    personId: int
    eventId: int

# Delete Event endpoint
@app.delete("/events/{event_id}")
async def delete_event(event_id: int):
    try:
        db.delete_event(event_id)  # Calls the delete method in dbObject
        return {"message": "Event deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete Participation endpoint
@app.delete("/participations/")
async def delete_participation(person_id: int, event_id: int):
    try:
        db.delete_participation(person_id, event_id)  # Calls the delete method in dbObject
        return {"message": "Participation deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))