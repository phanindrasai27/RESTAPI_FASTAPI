from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient

app = FastAPI()

# Initialize MongoDB client and database
client = MongoClient("mongodb://localhost:27017/")
db = client["server_db"]
servers_collection = db["servers"]

# Define the Server model
class Server(BaseModel):
    name: str
    id: str
    language: str
    framework: str

# Create a server
@app.post("/servers/", response_model=Server)
def create_server(server: Server):
    result = servers_collection.insert_one(server.dict())
    server.id = str(result.inserted_id)
    return server

# Get all servers or a specific server by ID
@app.get("/servers/", response_model=List[Server])
def get_servers(id: str = None):
    if id:
        server = servers_collection.find_one({"id": id})
        if server:
            return [Server(**server)]
        else:
            raise HTTPException(status_code=404, detail="Server not found")
    else:
        return list(map(Server, servers_collection.find()))

# Update a server by ID
@app.put("/servers/{id}", response_model=Server)
def update_server(id: str, updated_server: Server):
    server = servers_collection.find_one({"id": id})
    if server:
        servers_collection.replace_one({"id": id}, updated_server.dict())
        updated_server.id = id
        return updated_server
    else:
        raise HTTPException(status_code=404, detail="Server not found")

# Delete a server by ID
@app.delete("/servers/{id}", response_model=Server)
def delete_server(id: str):
    server = servers_collection.find_one({"id": id})
    if server:
        servers_collection.delete_one({"id": id})
        return Server(**server)
    else:
        raise HTTPException(status_code=404, detail="Server not found")

@app.get("/servers/search/", response_model=List[Server])
def find_servers_by_name(name: str):
    servers = list(servers_collection.find({"name": {"$regex": name, "$options": "i"}}))
    if servers:
        return [Server(**server) for server in servers]
    else:
        raise HTTPException(status_code=404, detail="No servers found")

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
