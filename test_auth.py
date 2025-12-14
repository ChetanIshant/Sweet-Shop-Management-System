import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, init_db
from sqlmodel import SQLModel
from app import models

@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    # use a temporary sqlite file
    db_file = tmp_path / "test.db"
    url = f"sqlite:///{db_file}"
    monkeypatch.setenv("DATABASE_URL", url)
    # re-import database/engine
    init_db()
    yield

def test_register_and_login():
    client = TestClient(app)
    # register
    res = client.post("/api/auth/register", json={"username": "alice", "password": "secret", "is_admin": True})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data

    # login
    res2 = client.post("/api/auth/login", data={"username": "alice", "password": "secret"})
    assert res2.status_code == 200
    data2 = res2.json()
    assert "access_token" in data2

def test_register_duplicate():
    client = TestClient(app)
    res = client.post("/api/auth/register", json={"username": "bob", "password": "pass"})
    assert res.status_code == 200
    res2 = client.post("/api/auth/register", json={"username": "bob", "password": "pass"})
    assert res2.status_code == 400