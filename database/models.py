from sqlalchemy import Column, Integer, String, Boolean, func, Table, Text, ForeignKey, ARRAY, Float
import enum
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import Enum
from datetime import datetime

Base = declarative_base()

class StartGrowing(str, enum.Enum):
    direct = 'direct'
    transplant = 'transplant'
    other = 'not_selected'

class LandingPlace(str, enum.Enum):
    house = 'house'
    garden = 'garden'
    universal = 'universal'
    other = 'not_selected'

class Pollination(str, enum.Enum):
    self_pollination = 'self_pollination'
    hand_pollination = 'hand_pollination'
    allogamy = 'allogamy'
    other = 'not_selected'

class UseType(str, enum.Enum):
    canning = 'canning'
    cooking = 'cooking'
    freezing = 'freezing'
    fresh = 'fresh'
    other = 'not_selected'

class SunlightType(str, enum.Enum):
    partial_shade = 'partial_shade'
    shade = 'shade'
    light_side = 'light_side'
    other = 'not_selected'

class CountType(str, enum.Enum):
    gramms = 'gramms'
    pack = 'pack'
    quantity = 'quantity'

class SeedCategory(str, enum.Enum):
    vegetable = 'vegetable'
    herb = 'herb'
    flower = 'flower'
    other = 'other'

class SeedLifeCycle(str, enum.Enum):
    annual = 'annual'
    biennial = 'biennial'
    perennial = 'perennial'
    other = 'other'

class SeedCulture(str, enum.Enum):
    hybrid = 'hybrid'
    sort = 'sort'
    other = 'other'

class SeedVegetationPeriod(str, enum.Enum):
    early = 'early'
    mid_early = 'mid_early'
    average = 'average'
    late = 'late'
    other = 'other'

class SeedHeight(str, enum.Enum):
    short = 'short'
    medium = 'medium'
    tall = 'tall'
    other = 'other'

seed_m2m_seedcollection = Table(
    "seed_m2m_seedcollection",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("seed_id", Integer, ForeignKey("seeds.id", ondelete="CASCADE")),
    Column("seedcollection_id", Integer, ForeignKey("seeds_collection.id", ondelete="CASCADE")),
)

class Seed(Base):
    __tablename__ = 'seeds'
    
    id = Column(Integer, primary_key=True,unique=True)
    image_url = Column(String(255), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.now())
    note = Column(String, nullable=True)
    brand_name = Column(String, nullable=True)
    name = Column(String, nullable=False)
    up_to_date = Column(DateTime, nullable=True)
    count = Column(Float, nullable=True)
    count_type = Column(Enum('gramms','pack','quantity', name = "Count_type"),nullable=False, default='gramms')
    category = Column(Enum('vegetable','herb','flower','other', name = "category"), nullable=False, default='other')
    life_cycle = Column(Enum('annual','biennial','perennial','other', name = "life_cycle"), nullable=False, default='other')
    culture = Column(Enum('hybrid','sort','other', name = "culture"), nullable=False, default='other')
    vegetation_period = Column(Enum('early','mid_early','average','late','other', name = "vegetation_period"), nullable=False, default='other')
    height = Column(Enum('short','medium','tall','other', name = "height"), nullable=False, default='other')
    flowering_period_start = Column(DateTime, nullable=True)
    flowering_period_end = Column(DateTime, nullable=True)
    sow_period_start = Column(DateTime, nullable=True)
    sow_period_end = Column(DateTime, nullable=True)
    depth = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    length = Column(Float, nullable=True)
    germinate_days = Column(Integer, nullable=True)
    instructions = Column(String, nullable=True)
    is_pet_safe = Column(Boolean, nullable=True)
    is_native = Column(Boolean, nullable=True)
    soil_type = Column(String, nullable=True)
    start_growing = Column(Enum('direct','transplant','not_selected', name = "start_growing"), nullable=False, default='not_selected')
    landing_place = Column(Enum('house','garden','universal','not_selected', name = "landing_place"), nullable=False, default='not_selected')
    pollination = Column(Enum('self_pollination','hand_pollination','allogamy','not_selected', name = "pollination"), nullable=False, default='not_selected')
    use_type = Column(Enum('canning','cooking','freezing','fresh','not_selected', name = "use_type"), nullable=False, default='not_selected')
    sunlight = Column(Enum('partial_shade','shade','light_side','not_selected', name = "sunlight"), nullable=False, default='not_selected')
    # collection_id = Column(Integer, ForeignKey("seeds_collection.id", ondelete="CASCADE"),nullable=True)
    collection = relationship("SeedCollection",secondary=seed_m2m_seedcollection,back_populates="seeds")
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), default=None)


class SeedCollection(Base):
    __tablename__ = "seeds_collection"

    id = Column(Integer, primary_key=True,unique=True)
    collection_name = Column(String, nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), default=None)
    seeds = relationship("Seed", secondary=seed_m2m_seedcollection, back_populates="collection")




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50),unique=True,nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=True)
    created_at = Column('created_at', DateTime, default=datetime.now)
    confirmed_email = Column(Boolean, default=False)
    refresh_token = Column(String(255), nullable=True)
    is_banned = Column(Boolean, default=False)
    seed = relationship("Seed", backref="users")
    collection = relationship("SeedCollection", backref="users")






