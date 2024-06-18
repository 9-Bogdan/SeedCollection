from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Dict,Optional
from sqlalchemy.orm import Session
from database.connect_db import get_db
import repository.seed_collection
from schemas.schemas import SeedCollectionCreate, SeedCollectionModelResponse
from database import models
from datetime import datetime
from services.auth import auth_service

router = APIRouter(prefix='/seed_collection', tags=['seed_collection'])

@router.post("/create_seed_collection", response_model = SeedCollectionCreate, status_code=status.HTTP_201_CREATED)
async def create_seed_collection(collection_name:str,date_created: Optional[datetime]= None, db:Session = Depends(get_db),current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    result = await repository.seed_collection.create_seed_collection(collection_name,date_created,db,current_user)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Seed collection already created")
    return result
    

@router.get("/find_seed_collection_by_id/{seed_collection_id}", response_model=SeedCollectionModelResponse)
async def find_seed_collection_by_id(seed_collection_id:int, db:Session = Depends(get_db),current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    result = await repository.seed_collection.find_seed_collection_by_id(seed_collection_id,db,current_user)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Seed collection not found")
    return  result

@router.get("list_of_all_seed_collections")
async def list_of_all_seed_collections(skip: int = 0, limit: int = 50,db: Session = Depends(get_db),current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    result = await repository.seed_collection.list_of_all_seed_collections(skip,limit,db,current_user)
    return {"seed_collections":result}

@router.put("/update_seed_collection/{collection_id}", response_model=SeedCollectionModelResponse)
async def update_seed_collection(collection_id:int, change_name:Optional[str] = None,change_date:Optional[datetime]=None, db:Session = Depends(get_db),current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    result = await repository.seed_collection.update_seed_collection(collection_id,change_name,change_date,db,current_user)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Seed collection not found")
    else:
        return result

@router.delete("/delete_seed_collection/{collection_id}")
async def delete_seed_collection(collection_id:int, db:Session = Depends(get_db),current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    result = await repository.seed_collection.delete_seed_collection(collection_id, db,current_user)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Seed not found")
    return {collection_id: "Seed collection deleted"}
    

@router.post("/add_seed_to_collection",response_model=SeedCollectionModelResponse)
async def add_seed_to_collection(seed_id:int, collection_id:int, db:Session = Depends(get_db),current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    result = await repository.seed_collection.add_seed_to_collection(seed_id, collection_id, db,current_user)
    if result == "Collection":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This collection does not exist")
    elif result == "Seed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This seed does not exist")
    elif result == "Seed-Collection":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This seed is already in this collection")
    return result

@router.delete("/delete_seed_from_collection", response_model=SeedCollectionModelResponse)
async def delete_seed_from_collection(seed_id:int, collection_id:int, db:Session = Depends(get_db),current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    result = await repository.seed_collection.delete_seed_from_collection(seed_id, collection_id, db,current_user)
    if result == "Collection":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This collection does not exist")
    elif result == "Seed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This seed does not exist")
    elif result == "Seed-Collection":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This seed is not in this collection")
    else:
        return result
