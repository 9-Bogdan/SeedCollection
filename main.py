import uvicorn
from fastapi import FastAPI, Request
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from fastapi_limiter import FastAPILimiter
import redis

from conf.config import settings
from database.connect_db import get_db
from routes import seeds,seed_collection,auth

app = FastAPI()

from fastapi_sso.sso.google import GoogleSSO
from database.models import User
from services.auth import auth_service
from fastapi.responses import RedirectResponse, JSONResponse
CLIENT_ID = settings.client_id
CLIENT_SECRET = settings.client_secret
google_sso = GoogleSSO(CLIENT_ID, CLIENT_SECRET, "http://localhost:8000/google/callback")

@app.get("/google/login_with_sso")
async def google_login():
    with google_sso:
        return await google_sso.get_login_redirect()

@app.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    with google_sso:
        user_info = await google_sso.verify_and_process(request)
    
    if not user_info:
        raise HTTPException(status_code=400, detail="Google login failed")

    email = user_info.email
    name = user_info.display_name

    # Перевірка, чи існує користувач у базі даних
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        # Якщо користувача немає, створити нового
        user = User(email=email, username=name, confirmed_email = True)
        db.add(user)
        db.commit()
        db.refresh(user)

    #Створення токенів доступу і оновлення
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Welcome to SeedsApp!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")
    
app.include_router(auth.router, prefix='/api')
app.include_router(seeds.router, prefix='/api')
app.include_router(seed_collection.router, prefix='/api')




