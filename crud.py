from sqlmodel import select
from . import models, auth
from fastapi import HTTPException

def get_user(session, username):
    return session.exec(select(models.User).where(models.User.username==username)).first()

def create_user(session, u, is_verified: bool = True):
    user = models.User(
        username=u.username,
        hashed_password=auth.get_password_hash(u.password),
        is_admin=u.is_admin,
        is_verified=is_verified
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def auth_user(session, u, p):
    user = get_user(session, u)
    if not user or not auth.verify_password(p, user.hashed_password):
        return None
    return user

# Sweets CRUD

def create_sweet(session, s):
    sweet = models.Sweet(
        name=s.name,
        category=s.category,
        price=s.price,
        quantity=s.quantity
    )
    session.add(sweet)
    session.commit()
    session.refresh(sweet)
    return sweet

def list_sweets(session):
    return session.exec(select(models.Sweet)).all()

def get_sweet(session, sweet_id):
    return session.get(models.Sweet, sweet_id)

def purchase_sweet(session, sweet_id, quantity=1):
    sweet = get_sweet(session, sweet_id)
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    if sweet.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    sweet.quantity -= quantity
    session.add(sweet)
    session.commit()
    session.refresh(sweet)
    return sweet

def restock_sweet(session, sweet_id, quantity=1):
    sweet = get_sweet(session, sweet_id)
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    sweet.quantity += quantity
    session.add(sweet)
    session.commit()
    session.refresh(sweet)
    return sweet

def delete_sweet(session, sweet_id):
    sweet = get_sweet(session, sweet_id)
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    session.delete(sweet)
    session.commit()
    return True