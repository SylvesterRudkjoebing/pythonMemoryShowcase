import sys
from models import Person, Event, DatabaseManager

class Node():
    """ Node class that represents a state, its parent state and the action that when applied to the parent resulted in this state """

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    """ Stack Frontier Class that represents states to be expanded during the search. The stack frontier uses a last-in first out ordering to determine the next state to expand when searching for solutions. This results in a Depth-First Search type algorithm """

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    """ Queue Frontier Class, which extends the StackFrontier class. It uses a first-in first-out ordering to determine the next state to expand when searching for solutions. This results in a Breadth-First Search type algorithm """

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class bfsObject:
    def __init__(self, conn):
        # Accept the connection as a parameter
        self.conn = conn
        self.db_manager = DatabaseManager()

        # Maps names to a set of corresponding person_ids
        self.names = {}

        # Maps person_ids to a dictionary of: name, birth, events (a set of event_ids)
        self.people = {}

        # Maps event_ids to a dictionary of: event, year, participations (a set of person_ids)
        self.events = {}

    def load_data(self, database):
        """
        Load data from SQLite database into memory using SQLAlchemy.
        """
        session = self.db_manager.get_session()
        try:
            # Load people
            people = session.query(Person).all()
            for person in people:
                self.people[person.id] = {
                    "name": person.name,
                    "birth": person.birth,
                    "events": {event.id for event in person.events}
                }
                name_lower = person.name.lower()
                if name_lower not in self.names:
                    self.names[name_lower] = {person.id}
                else:
                    self.names[name_lower].add(person.id)

            # Load events
            events = session.query(Event).all()
            for event in events:
                self.events[event.id] = {
                    "event": event.event,
                    "year": event.year,
                    "participations": {person.id for person in event.participants}
                }
        finally:
            session.close()


    def person_id_for_name(self, name):
        """
        Returns the person id for a person's name,
        resolving ambiguities as needed.
        """
        person_ids = list(self.names.get(name.lower(), set()))
        if len(person_ids) == 0:
            return None
        elif len(person_ids) > 1:
            print(f"Which '{name}'?")
            session = self.db_manager.get_session()
            try:
                for person_id in person_ids:
                    person = session.query(Person).filter(Person.id == person_id).first()
                    print(f"ID: {person.id}, Name: {person.name}, Birth: {person.birth}")
                
                try:
                    person_id = input("Intended Person ID: ")
                    if person_id in person_ids:
                        return int(person_id)
                except ValueError:
                    pass
                return None
            finally:
                session.close()
        else:
            return person_ids[0]

    def neighbors_for_person(self, person_id):
        """
        Returns (event_id, person_id) pairs for people
        who starred with a given person.
        """
        event_ids = self.people[person_id]["events"]
        neighbors = set()
        for event_id in event_ids:
            for co_star_id in self.events[event_id]["participations"]:
                neighbors.add((event_id, co_star_id))
        return neighbors

    def shortest_path(self, source, target):
        """
        Returns the shortest list of (event_id, person_id) pairs
        that connect the source to the target, using BFS.

        source and target are unique IMDB actor ID's

        If no possible path, returns None.
        """
        # Initialise a QueueFrontier for BFS, with the starting actor ID:
        start = Node(source, None, None)
        frontier = QueueFrontier()
        frontier.add(start)

        # Initialise an empty explored set to hold explored states (actors):
        explored = set()

        # Loop until a solution is found, or Frontier is empty(no solution):
        while True:

            if len(explored) % 100 == 0:
                print('Venner explored to find solution: ', len(explored))
                print('Nodes left to expand in Frontier: ', len(frontier.frontier))

            # Check for empty Frontier and return with no path if empty
            if frontier.empty():
                print('Frontier is Empty - No Connection Between Actors!')
                print(len(explored), 'actors explored to with no solution found!')
                return None

            # Otherwise expand the next node in the Queue, add it to the explored states and get set of events and actors for the actor in the current node:
            curr_node = frontier.remove()
            explored.add(curr_node.state)

            for action, state in self.neighbors_for_person(curr_node.state):

                # If state (actor) is the target actor then solution has been found, return path:
                if state == target:
                    print('Solution Found!')
                    print(len(explored), 'venner explored to find solution!')
                    # Create path from source to target
                    path = []
                    path.append((action, state))

                    # Add action and state to path until back to start node
                    while curr_node.parent != None:
                        path.append((curr_node.action, curr_node.state))
                        curr_node = curr_node.parent

                    path.reverse()

                    return path

                # Otherwise add the new states to explore to the frontier:
                if not frontier.contains_state(state) and state not in explored:
                    new_node = Node(state, curr_node, action)
                    frontier.add(new_node)

    def calculate(self, target_name):
        """
        Main function to calculate the shortest path.
        """
        database = "MemoryDB.db"

        # Load data from database into memory
        print("Loading data...")
        self.load_data(database)
        print("Data loaded.")
        
        # Hardcoder source name til Mikkel for dataens skyld.
        source_name = "Mikkel"

        source = self.person_id_for_name(source_name)
        if source is None:
            sys.exit("Person not found.")
        
        target = self.person_id_for_name(target_name)
        if target is None:
            sys.exit("Person not found.")

        path = self.shortest_path(source, target)

        if path is None:
            print("Not connected.")
            relations = []
        else:
            degrees = len(path)
            print(f"{degrees} degrees of separation.")
            path = [(None, source)] + path
            relations = []
            for i in range(degrees):
                person1 = self.people[path[i][1]]["name"]
                person2 = self.people[path[i + 1][1]]["name"]
                event = self.events[path[i + 1][0]]["event"]
                if i == 0:
                    relation = f"You og {person2} met {event}"
                else:
                    relation = f"{person1} introduced you to {person2} {event}"
                print(relation)
                relations.append(relation)

        return relations




