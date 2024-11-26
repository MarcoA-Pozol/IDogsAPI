from fastapi import APIRouter, HTTPException, Depends 
from app.schemas import Breed
from app.database import get_database
from bson import ObjectId
from typing import List
# Cache functions
from ..redis.utils import save_hash, get_hash, delete_hash

router = APIRouter()

# List breeds
@router.get("/breeds/", response_model=List[Breed])
async def list_breeds():
    """
        List all breeds from MongoDB breeds collection and retrieve it.
    """
    
    db = await get_database()
    list_of_breeds = await db["breeds"].find().to_list(50)
    
    if list_of_breeds is None:
        raise HTTPException(status_code=404, detail="No breeds found.")
    
    # Convert MongoDB documents to Breed objects
    return [
        Breed(id=str(breed["_id"]), **{key: breed[key] for key in breed if key != "_id"})
        for breed in list_of_breeds
    ]
    
# Retrieve specific breed
@router.get("/breeds/{breed_id}", response_model=Breed)
async def retrieve_breed(breed_id):
    """
        Retrieves a specific Breed by their ObjectID.
    """
    try:
        # Check if requested object exists in cache and get it
        data = get_hash(key=breed_id)
        print(f"Fetching data from Cache: {data}")
        # If not exists in cache, get from DB
        if not data:
            db = await get_database()
            # Convert dog id from string to ObjectId (MongoDB as another no-relational databases uses a different ID type)
            try:
                obj_id = ObjectId(breed_id)
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid ObjectID format")
            breed = await db["breeds"].find_one({"_id": obj_id}) # MongoDB query using ObjectId
            
            print(f"Fetching data from Database: {breed}")
            # Save on cache with Redis
            if breed:
                # Save on cache the retrieved data from the database
                save_hash(breed_id, breed)
                data = breed
            else:
                raise HTTPException(status_code=404, detail="Breed not found")
        return Breed(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")    

        
@router.post("/breeds/", response_model=Breed)
async def create_breed(breed: Breed):
    """
    Creates a new breed.
    """
    db = await get_database()

    try:
        # Save on database with MongoDB
        result = await db["breeds"].insert_one(breed.model_dump())
        
        if result.acknowledged:
            # Fetch saved object from MongoDB
            fetched_breed = await db["breeds"].find_one({"_id": result.inserted_id})
            
            if fetched_breed:
                # Transform MongoDB `_id` to string for JSON compatibility
                fetched_breed["_id"] = str(fetched_breed["_id"])

                # Save on cache with Redis
                save_hash(key=fetched_breed["_id"], data=fetched_breed)

                # Return the fetched document
                return fetched_breed
            else:
                raise HTTPException(status_code=404, detail="Breed not found after insertion")
        else:
            raise HTTPException(status_code=500, detail="Breed not created")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
