from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Dict,Optional
from sqlalchemy.orm import Session
from database.connect_db import get_db
import repository.seeds
from schemas.schemas import SeedModelDb, SeedModelResponse,SeedModelResponseList, SeedModelUpdate
from database import models
from datetime import datetime
from services.auth import auth_service

router = APIRouter(prefix='/seeds', tags=['seeds'])


@router.post("/create_seed", response_model = SeedModelResponse, status_code=status.HTTP_201_CREATED)
async def create_seed(image_url: str,name: str, date_created: Optional[datetime]= None,
                      note: Optional[str]= None,brand_name: Optional[str]= None,up_to_date: Optional[datetime]= None,count: Optional[float]= None,
                      flowering_period_start: Optional[datetime]= None,flowering_period_end: Optional[datetime]= None,
                      sow_period_start: Optional[datetime]= None,sow_period_end: Optional[datetime]= None,
                      depth: Optional[float]= None,width: Optional[float]= None,length: Optional[float]= None,germinate_days: Optional[int]= None,
                      instructions: Optional[str]= None,is_pet_safe: Optional[bool]= None,is_native: Optional[bool]= None,soil_type: Optional[str]= None,
                      count_type: models.CountType = Query(None, description="Count type"),
                      category: models.SeedCategory = Query(None, description="Category"),
                      life_cycle: models.SeedLifeCycle = Query(None, description="Life cycle"),
                      culture: models.SeedCulture = Query(None, description="Culture"),
                      vegetation_period: models.SeedVegetationPeriod = Query(None, description="Vegetation period"),
                      height: models.SeedHeight = Query(None, description="Height"),
                      start_growing: models.StartGrowing = Query(None, description="Starting growing"),
                      landing_place: models.LandingPlace = Query(None, description="Landing Place"),
                      pollination: models.Pollination = Query(None, description="Pollination"),
                      use_type: models.UseType = Query(None, description="Use Type"),
                      sunlight: models.SunlightType = Query(None, description="Sunlight"),
                      db: Session = Depends(get_db),
                      current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    return await repository.seeds.create_seed(image_url,date_created,name,note,brand_name,up_to_date,count,
                      flowering_period_start,flowering_period_end,sow_period_start,sow_period_end,
                      depth,width,length,germinate_days,instructions,is_pet_safe,is_native,soil_type,
                      count_type,category,life_cycle,culture,vegetation_period,height,start_growing,landing_place,
                      pollination,use_type,sunlight, db,current_user)

@router.get("/find_seeds_by_id/{seed_id}", response_model=SeedModelResponse)
async def find_seeds_by_name(seed_id: int, db: Session = Depends(get_db),current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    result = await repository.seeds.find_seed_by_id(seed_id, db,current_user)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Seed not found")
    return result

@router.get("/list_of_all_seeds", response_model=SeedModelResponseList)
async def list_of_all_seeds(skip: int = 0, limit: int = 50,db: Session = Depends(get_db),current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    result = await repository.seeds.list_of_all_seeds(skip,limit,db,current_user)
    return {"seeds":result}

@router.put("/update_seed/{seed_id}")
async def update_seed(seed_id: int, image_url: Optional[str] = None,name: Optional[str] = None,
                      note: Optional[str]= None,brand_name: Optional[str]= None,up_to_date: Optional[datetime]= None,count: Optional[float]= None,
                      flowering_period_start: Optional[datetime]= None,flowering_period_end: Optional[datetime]= None,
                      sow_period_start: Optional[datetime]= None,sow_period_end: Optional[datetime]= None,
                      depth: Optional[float]= None,width: Optional[float]= None,length: Optional[float]= None,germinate_days: Optional[int]= None,
                      instructions: Optional[str]= None,is_pet_safe: Optional[bool]= None,is_native: Optional[bool]= None,soil_type: Optional[str]= None,
                      count_type: models.CountType = Query(None, description="Count type"),
                      category: models.SeedCategory = Query(None, description="Category"),
                      life_cycle: models.SeedLifeCycle = Query(None, description="Life cycle"),
                      culture: models.SeedCulture = Query(None, description="Culture"),
                      vegetation_period: models.SeedVegetationPeriod = Query(None, description="Vegetation period"),
                      height: models.SeedHeight = Query(None, description="Height"),
                      start_growing: models.StartGrowing = Query(None, description="Starting growing"),
                      landing_place: models.LandingPlace = Query(None, description="Landing Place"),
                      pollination: models.Pollination = Query(None, description="Pollination"),
                      use_type: models.UseType = Query(None, description="Use Type"),
                      sunlight: models.SunlightType = Query(None, description="Sunlight"), db: Session = Depends(get_db),
                      current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    result = await repository.seeds.update_seed(seed_id,image_url,name,note,brand_name,up_to_date,count,
                      flowering_period_start,flowering_period_end,sow_period_start,sow_period_end,
                      depth,width,length,germinate_days,instructions,is_pet_safe,is_native,soil_type,
                      count_type,category,life_cycle,culture,vegetation_period,height,start_growing,landing_place,
                      pollination,use_type,sunlight, db,current_user)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Seed not found")
    return result

@router.delete("/delete_seed/{seed_id}")
async def delete_seed(seed_id: int, db:Session = Depends(get_db),current_user: models.User = Depends(auth_service.get_current_user),
                      token: str = Depends(auth_service.oauth2_scheme)):
    if await auth_service.is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are logout")
    result = await repository.seeds.delete_seed(seed_id, db,current_user)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Seed not found")
    return {seed_id: "Seed deleted"}
                            
    
