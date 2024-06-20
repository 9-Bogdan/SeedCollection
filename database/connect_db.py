from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from conf.config import settings

# SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
POSTGRES_DB=settings.postgres
POSTGRES_USER=vatrupzn
POSTGRES_PASSWORD=pOyqg24qPVdWL0gaKD3lKgPhtcaM1AYR
POSTGRES_PORT=5432
POSTGRES_HOST=abul.db.elephantsql.com

engine = create_engine(f"postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()