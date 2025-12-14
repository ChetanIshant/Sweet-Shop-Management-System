import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
from pathlib import Path
import os

@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")
    init_db()
    yield

def get_token(client, username="admin", password="secret", is_admin=True):
    client.post("/api/auth/register", json={"username": username, "password": password, "is_admin": is_admin})
    res = client.post("/api/auth/login", data={"username": username, "password": password})
    return res.json()["access_token"]

def test_add_list_and_purchase():
    client = TestClient(app)
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    # add sweet
    res = client.post("/api/sweets", json={"name": "Chocolate", "category": "Candy", "price": 2.5, "quantity": 10}, headers=headers)
    assert res.status_code == 200
    s = res.json()
    assert s["name"] == "Chocolate"

    # list
    res2 = client.get("/api/sweets", headers=headers)
    assert res2.status_code == 200
    assert len(res2.json()) == 1

    # purchase
    sweet_id = s["id"]
    res3 = client.post(f"/api/sweets/{sweet_id}/purchase", params={"quantity": 3}, headers=headers)
    assert res3.status_code == 200
    assert res3.json()["quantity"] == 7

def test_restock_and_delete_admin_checks():
    client = TestClient(app)
    admin_token = get_token(client, "admin2", "pw", True)
    user_token = get_token(client, "user1", "pw", False)
    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    headers_user = {"Authorization": f"Bearer {user_token}"}

    # Add sweet as admin
    res = client.post("/api/sweets", json={"name": "Lollipop", "category": "Candy", "price": 1.0, "quantity": 5}, headers=headers_admin)
    s = res.json()
    sid = s["id"]

    # user cannot restock
    res_user_restock = client.post(f"/api/sweets/{sid}/restock", params={"quantity": 10}, headers=headers_user)
    assert res_user_restock.status_code == 403

    # admin can restock
    res_admin_restock = client.post(f"/api/sweets/{sid}/restock", params={"quantity": 10}, headers=headers_admin)
    assert res_admin_restock.status_code == 200
    assert res_admin_restock.json()["quantity"] == 15

    # non-admin cannot delete
    res_user_delete = client.delete(f"/api/sweets/{sid}", headers=headers_user)
    assert res_user_delete.status_code == 403

    # admin delete
    res_admin_delete = client.delete(f"/api/sweets/{sid}", headers=headers_admin)
    assert res_admin_delete.status_code == 200