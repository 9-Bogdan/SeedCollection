from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, constr, SecretStr, validator

from database.models import Seed
from database import models

# class SeedModelDb(BaseModel):
#     image_url: str
#     date_created: Optional[datetime] = None
#     name: str
#     count_type: models.CountType
#     category: models.SeedCategory
#     life_cycle: models.SeedLifeCycle
#     culture: models.SeedCulture
#     vegetation_period: models.SeedVegetationPeriod
#     height: models.SeedHeight
#     start_growing: models.StartGrowing
#     landing_place: models.LandingPlace
#     pollination: models.Pollination
#     use_type: models.UseType
#     sunlight: models.SunlightType
#     note: Optional[str] = None
#     brand_name: Optional[str] = None
#     up_to_date: Optional[datetime] = None
#     count: Optional[float] = None
#     flowering_period_start: Optional[datetime] = None
#     flowering_period_end: Optional[datetime] = None
#     sow_period_start: Optional[datetime] = None
#     sow_period_end: Optional[datetime] = None
#     depth: Optional[float] = None
#     width: Optional[float] = None
#     length: Optional[float] = None
#     germinate_days: Optional[int] = None
#     instructions: Optional[str] = None
#     is_pet_safe: Optional[bool] = None
#     is_native: Optional[bool] = None
#     soil_type: Optional[str] = None

#     class Config:
#         from_attributes = True
#         use_enum_values = True
class SeedModelDb(BaseModel):
    image_url: str
    date_created: Optional[datetime] = None
    name: str
    count_type: str
    category: str
    life_cycle: str
    culture: str
    vegetation_period: str
    height: str
    start_growing: str
    landing_place: str
    pollination: str
    use_type: str
    sunlight: str
    note: Optional[str] = None
    brand_name: Optional[str] = None
    up_to_date: Optional[datetime] = None
    count: Optional[float] = None
    flowering_period_start: Optional[datetime] = None
    flowering_period_end: Optional[datetime] = None
    sow_period_start: Optional[datetime] = None
    sow_period_end: Optional[datetime] = None
    depth: Optional[float] = None
    width: Optional[float] = None
    length: Optional[float] = None
    germinate_days: Optional[int] = None
    instructions: Optional[str] = None
    is_pet_safe: Optional[bool] = None
    is_native: Optional[bool] = None
    soil_type: Optional[str] = None
    collection_id: Optional[int] = None

    class Config:
        from_attributes = True
        orm_mode = True

class SeedModelResponse(BaseModel):
    id: int
    image_url: str
    date_created: datetime
    note: Optional[str]
    brand_name: Optional[str]
    name: str
    up_to_date: Optional[datetime]
    count: Optional[float]
    count_type: str
    category: str
    life_cycle: str
    culture: str
    vegetation_period: str
    height: str
    flowering_period_start: Optional[datetime]
    flowering_period_end: Optional[datetime]
    sow_period_start: Optional[datetime]
    sow_period_end: Optional[datetime]
    depth: Optional[float]
    width: Optional[float]
    length: Optional[float]
    germinate_days: Optional[int]
    instructions: Optional[str]
    is_pet_safe: Optional[bool]
    is_native: Optional[bool]
    soil_type: Optional[str]
    start_growing: str
    landing_place: str
    pollination: str
    use_type: str
    sunlight: str
    # collection_id: Optional[int]

    detail: str="Seed successfully created"

class SeedModelResp(BaseModel):
    id: int
    name: str

class SeedModelResponseList(BaseModel):
    seeds: List[SeedModelResponse]

class SeedModelUpdate(BaseModel):
    image_url: str
    date_created: Optional[datetime] = None
    name: str
    count_type: str
    category: str
    life_cycle: str
    culture: str
    vegetation_period: str
    height: str
    start_growing: str
    landing_place: str
    pollination: str
    use_type: str
    sunlight: str
    note: Optional[str] = None
    brand_name: Optional[str] = None
    up_to_date: Optional[datetime] = None
    count: Optional[float] = None
    flowering_period_start: Optional[datetime] = None
    flowering_period_end: Optional[datetime] = None
    sow_period_start: Optional[datetime] = None
    sow_period_end: Optional[datetime] = None
    depth: Optional[float] = None
    width: Optional[float] = None
    length: Optional[float] = None
    germinate_days: Optional[int] = None
    instructions: Optional[str] = None
    is_pet_safe: Optional[bool] = None
    is_native: Optional[bool] = None
    soil_type: Optional[str] = None
    # collection_id: Optional[int] = None

    class Config:
        from_attributes = True

class SeedCollectionCreate(BaseModel):
    id: int
    collection_name: str
    created_date: datetime

class SeedCollectionModelResponse(BaseModel):
    id: int
    collection_name: str
    created_date: datetime
    seeds: List[SeedModelResp]

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)

class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class UserUpdate(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)
    password: SecretStr


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
