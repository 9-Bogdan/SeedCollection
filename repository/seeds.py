from datetime import datetime
from typing import List
from fastapi import UploadFile, status
from sqlalchemy import and_, desc
from sqlalchemy.orm import Session, joinedload
from fastapi.exceptions import HTTPException

from database.models import Seed, User
from conf.config import settings
from schemas.schemas import SeedModelDb, SeedModelResponse, SeedModelUpdate

async def create_seed(image_url_,date_created_,name_,note_,brand_name_,up_to_date_,count_,
                      flowering_period_start_,flowering_period_end_,sow_period_start_,sow_period_end_,
                      depth_,width_,length_,germinate_days_,instructions_,is_pet_safe_,is_native_,soil_type_,
                      count_type_,category_,life_cycle_,culture_,vegetation_period_,height_,start_growing_,landing_place_,
                      pollination_,use_type_,sunlight_, db: Session,current_user: User) -> Seed:
    seed = Seed(image_url = image_url_,
    date_created = date_created_,
    note = note_,
    brand_name = brand_name_,
    name = name_,
    up_to_date = up_to_date_,
    count = count_,
    count_type = count_type_,
    category = category_,
    life_cycle = life_cycle_,
    culture = culture_,
    vegetation_period = vegetation_period_, 
    height = height_,
    flowering_period_start = flowering_period_start_,
    flowering_period_end = flowering_period_end_,
    sow_period_start = sow_period_start_,
    sow_period_end = sow_period_end_,
    depth = depth_,
    width = width_,
    length = length_,
    germinate_days = germinate_days_,
    instructions = instructions_,
    is_pet_safe = is_pet_safe_,
    is_native = is_native_,
    soil_type = soil_type_,
    start_growing = start_growing_,
    landing_place = landing_place_,
    pollination = pollination_,
    use_type = use_type_,
    sunlight = sunlight_,
    user_id = current_user.id)
    db.add(seed)
    db.commit()
    db.refresh(seed)
    return seed

async def find_seed_by_id(seed_id: int, db:Session,current_user: User):
    seed = db.query(Seed).filter(Seed.id == seed_id, Seed.user_id == current_user.id).first()
    if seed is None:
        return None
    return seed

async def list_of_all_seeds(skip: int, limit: int, db: Session,current_user: User) -> List[Seed]:
    return db.query(Seed).filter(Seed.user_id == current_user.id).offset(skip).limit(limit).all()

async def update_seed(seed_id: int,image_url_,name_,note_,brand_name_,up_to_date_,count_,
                      flowering_period_start_,flowering_period_end_,sow_period_start_,sow_period_end_,
                      depth_,width_,length_,germinate_days_,instructions_,is_pet_safe_,is_native_,soil_type_,
                      count_type_,category_,life_cycle_,culture_,vegetation_period_,height_,start_growing_,landing_place_,
                      pollination_,use_type_,sunlight_, db:Session,current_user: User) -> Seed:
    seed = db.query(Seed).filter(Seed.id == seed_id).first()
    if seed is not None:
        if image_url_ is not None:
            seed.image_url = image_url_
        seed.date_created = seed.date_created,
        if note_ is not None:
            seed.note = note_
        if brand_name_ is not None:
            seed.brand_name = brand_name_
        if name_ is not None:
            seed.name = name_
        if up_to_date_ is not None:
            seed.up_to_date = up_to_date_
        if count_ is not None:
            seed.count = count_
        if count_type_ is not None:
            seed.count_type = count_type_
        if category_ is not None:
            seed.category = category_
        if life_cycle_ is not None:
            seed.life_cycle = life_cycle_
        if culture_ is not None:
            seed.culture = culture_
        if vegetation_period_ is not None:
            seed.vegetation_period = vegetation_period_
        if height_ is not None:
            seed.height = height_
        if flowering_period_start_ is not None:
            seed.flowering_period_start = flowering_period_start_
        if flowering_period_end_ is not None:
            seed.flowering_period_end = flowering_period_end_
        if sow_period_start_ is not None:
            seed.sow_period_start = sow_period_start_
        if sow_period_end_ is not None:
            seed.sow_period_end = sow_period_end_
        if depth_ is not None:
            seed.depth = depth_
        if width_ is not None:
            seed.width = width_
        if length_ is not None:
            seed.length = length_
        if germinate_days_ is not None:
            seed.germinate_days = germinate_days_
        if instructions_ is not None:
            seed.instructions = instructions_
        if is_pet_safe_ is not None:
            seed.is_pet_safe = is_pet_safe_
        if is_native_ is not None:
            seed.is_native = is_native_
        if soil_type_ is not None:
            seed.soil_type = soil_type_
        if start_growing_ is not None:
            seed.start_growing = start_growing_
        if landing_place_ is not None:
            seed.landing_place = landing_place_
        if pollination_ is not None:
            seed.pollination = pollination_
        if use_type_ is not None:
            seed.use_type = use_type_
        if sunlight_ is not None:
            seed.sunlight = sunlight_
        db.commit()
        db.refresh(seed)
        return seed
    
    

async def delete_seed(seed_id: int, db:Session,current_user: User):
    seed = db.query(Seed).filter(Seed.id == seed_id, Seed.user_id == current_user.id).first()
    if seed is None:
        return None
    db.delete(seed)
    db.commit()
    return {"message":"Seed deleted"}
