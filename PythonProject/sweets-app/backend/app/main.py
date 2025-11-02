from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta

from .database import connect_to_mongo, close_mongo_connection
from .schemas import UserCreate, Token, SweetCreate, SweetOut, LoginCredentials
from .auth import (
    get_password_hash, verify_password,
    create_access_token, get_current_active_user, get_admin_user
)
from .crud import (
    create_user, get_user_by_email, create_sweet, list_sweets,
    search_sweets, update_sweet, delete_sweet,
    get_sweet_by_id, purchase_sweet, restock_sweet
)
from .config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title="Sweets Shop API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/auth/register", status_code=201)
async def register(user: UserCreate):
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = await get_password_hash(user.password)
    created = await create_user(user.email, hashed, user.is_admin)
    return {"id": str(created["_id"]), "email": created["email"], "is_admin": created["is_admin"]}

@app.post("/api/auth/login", response_model=Token)
async def login(credentials: LoginCredentials):
    user = await get_user_by_email(credentials.email)
    if not user or not await verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        {"sub": str(user["_id"]), "is_admin": user.get("is_admin", False)},
        expires_delta=access_token_expires
    )
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/sweets", response_model=SweetOut)
async def add_sweet(sweet: SweetCreate, current_user=Depends(get_admin_user)):
    return await create_sweet(sweet)

@app.get("/api/sweets", response_model=list[SweetOut])
async def get_all_sweets(current_user=Depends(get_current_active_user)):
    return await list_sweets()

@app.get("/api/sweets/search", response_model=list[SweetOut])
async def search_all_sweets(
    name: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    current_user=Depends(get_current_active_user)
):
    return await search_sweets(name, category, min_price, max_price)

@app.put("/api/sweets/{sweet_id}", response_model=SweetOut)
async def update_sweet_details(sweet_id: str, sweet: SweetCreate, current_user=Depends(get_admin_user)):
    updated = await update_sweet(sweet_id, sweet)
    if not updated:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return updated

@app.delete("/api/sweets/{sweet_id}")
async def delete_sweet_item(sweet_id: str, current_user=Depends(get_admin_user)):
    deleted = await delete_sweet(sweet_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return {"message": "Sweet deleted successfully"}

@app.post("/api/sweets/{sweet_id}/purchase")
async def purchase_sweet_item(sweet_id: str, quantity: int = 1, current_user=Depends(get_current_active_user)):
    sweet = await get_sweet_by_id(sweet_id)
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    if sweet["quantity"] < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    await purchase_sweet(sweet_id, quantity)
    return {"message": f"Purchased {quantity} of {sweet['name']}"}

@app.post("/api/sweets/{sweet_id}/restock")
async def restock_sweet_item(sweet_id: str, quantity: int = 1, current_user=Depends(get_admin_user)):
    sweet = await get_sweet_by_id(sweet_id)
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    await restock_sweet(sweet_id, quantity)
    return {"message": f"Restocked {quantity} of {sweet['name']}"}
