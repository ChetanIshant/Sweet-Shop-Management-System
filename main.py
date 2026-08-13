from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from . import schemas, crud, auth
from .database import init_db, get_session
from .deps import get_current_user

from typing import List

app = FastAPI()

# allow local dev frontend to talk to backend
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.on_event("startup")
def start(): init_db()

@app.post("/api/auth/register", response_model=schemas.Token)
def register(u: schemas.UserCreate, session=Depends(get_session), auto_validate: bool = True):
    """
    Create a new user. Query param auto_validate (default True) controls whether the
    user is marked verified immediately. The endpoint returns an access token so the
    client can use it immediately (auto-login).
    """
    user = crud.create_user(session, u, is_verified=auto_validate)
    return {"access_token": auth.create_access_token(user.username), "token_type":"bearer"}

@app.post("/api/auth/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):
    user = crud.auth_user(session, form.username, form.password)
    if not user: raise HTTPException(400, "Invalid creds")
    return {"access_token": auth.create_access_token(user.username), "token_type":"bearer"}

@app.get("/api/auth/me")
def me(user=Depends(get_current_user)):
    return {"username": user.username, "is_admin": user.is_admin, "is_verified": user.is_verified}

# Sweets endpoints

@app.post("/api/sweets", response_model=schemas.SweetRead)
def create_sweet_endpoint(s: schemas.SweetCreate, user=Depends(get_current_user), session=Depends(get_session)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return crud.create_sweet(session, s)

@app.get("/api/sweets", response_model=List[schemas.SweetRead])
def list_sweets_endpoint(user=Depends(get_current_user), session=Depends(get_session)):
    return crud.list_sweets(session)

@app.post("/api/sweets/{sweet_id}/purchase", response_model=schemas.SweetRead)
def purchase_sweet_endpoint(sweet_id: int, quantity: int = 1, user=Depends(get_current_user), session=Depends(get_session)):
    # anyone authenticated and verified can purchase
    return crud.purchase_sweet(session, sweet_id, quantity)

@app.post("/api/sweets/{sweet_id}/restock", response_model=schemas.SweetRead)
def restock_sweet_endpoint(sweet_id: int, quantity: int = 1, user=Depends(get_current_user), session=Depends(get_session)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return crud.restock_sweet(session, sweet_id, quantity)
@app.delete("/api/sweets/{sweet_id}")
def delete_sweet_endpoint(sweet_id: int, user=Depends(get_current_user), session=Depends(get_session)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    crud.delete_sweet(session, sweet_id)
    return {"ok": True}
