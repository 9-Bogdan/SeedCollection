from datetime import datetime
from typing import List
from fastapi import UploadFile, status
from sqlalchemy import and_, desc
from sqlalchemy.orm import Session, joinedload
from fastapi.exceptions import HTTPException

from database.models import Seed, SeedCollection,User
from conf.config import settings
from schemas.schemas import SeedCollectionModelResponse, SeedModelResp

async def create_seed_collection(collection_name_, date_created_,db: Session,current_user:User) -> SeedCollection:
    already_created = db.query(SeedCollection).filter(SeedCollection.collection_name == collection_name_,SeedCollection.user_id == current_user.id).first()
    if already_created:
        return None
    else:
        collection = SeedCollection(
            collection_name = collection_name_,
            created_date = date_created_,
            user_id = current_user.id)
        db.add(collection)
        db.commit()
        db.refresh(collection)
        return collection

async def find_seed_collection_by_id(seed_collection_id,db:Session,current_user:User):
    collection = db.query(SeedCollection).filter(SeedCollection.id == seed_collection_id, SeedCollection.user_id == current_user.id).first()
    if collection is None:
        return None
    else:
        return SeedCollectionModelResponse(
        id=collection.id,
        collection_name=collection.collection_name,
        created_date=collection.created_date,
        seeds=[SeedModelResp(id=seed.id, name=seed.name) for seed in collection.seeds])

async def list_of_all_seed_collections(skip: int, limit: int,db: Session,current_user:User) -> List[SeedCollectionModelResponse]:
    seed_collections = db.query(SeedCollection).filter(SeedCollection.user_id == current_user.id).offset(skip).limit(limit).all()
    result = []
    for collection in seed_collections:
        seeds_names = [seed.name for seed in collection.seeds]
        collection_data = {
            "id": collection.id,
            "collection_name": collection.collection_name,
            "created_date": collection.created_date,
            "seeds": seeds_names}
        result.append(collection_data)
    return result


async def update_seed_collection(collection_id,change_name,change_date,db:Session,current_user:User):
    collection = db.query(SeedCollection).filter(SeedCollection.id == collection_id,SeedCollection.user_id == current_user.id).first()
    if collection is None:
        return None
    else:
        if change_name is not None:
            collection.collection_name = change_name
        if change_date is not None:
            collection.changed_date = change_date
        db.commit()
        db.refresh(collection)
        return SeedCollectionModelResponse(
        id=collection.id,
        collection_name=collection.collection_name,
        created_date=collection.created_date,
        seeds=[SeedModelResp(id=seed.id, name=seed.name) for seed in collection.seeds])

async def delete_seed_collection(collection_id, db:Session,current_user:User):
    collection = db.query(SeedCollection).filter(SeedCollection.id == collection_id,SeedCollection.user_id == current_user.id).first()
    if collection is None:
        return None
    db.delete(collection)
    db.commit()
    return {"message":"Seed deleted"}

async def add_seed_to_collection(seed_id, collection_id, db:Session,current_user:User):
    collection = db.query(SeedCollection).filter(SeedCollection.id == collection_id,SeedCollection.user_id == current_user.id).first()
    if collection is None:
        return "Collection"
    seed =  db.query(Seed).filter(Seed.id == seed_id,Seed.user_id == current_user.id).first()
    if seed is None:
        return "Seed"
    # if collection.id == seed.collection_id:
    #     return "Seed-Collection"
    if seed in collection.seeds:
        return "Seed-Collection"
    else:
        # seed.collection_id = collection.id
        collection.seeds.append(seed)
        db.commit()
        db.refresh(collection)
        return SeedCollectionModelResponse(
        id=collection.id,
        collection_name=collection.collection_name,
        created_date=collection.created_date,
        seeds=[SeedModelResp(id=seed.id, name=seed.name) for seed in collection.seeds])
    

async def delete_seed_from_collection(seed_id, collection_id, db:Session,current_user:User):
    collection = db.query(SeedCollection).filter(SeedCollection.id == collection_id,SeedCollection.user_id == current_user.id).first()
    if collection is None:
        return "Collection"
    seed =  db.query(Seed).filter(Seed.id == seed_id,Seed.user_id == current_user.id).first()
    if seed is None:
        return "Seed"
    # if collection.id != seed.collection_id:
    #     return "Seed-Collection"
    if seed not in collection.seeds:
        return "Seed-Collection"
    else:
        # seed.collection_id = None
        collection.seeds.remove(seed)
        db.commit()
        db.refresh(collection)
        return SeedCollectionModelResponse(
        id=collection.id,
        collection_name=collection.collection_name,
        created_date=collection.created_date,
        seeds=[SeedModelResp(id=seed.id, name=seed.name) for seed in collection.seeds])
    