import os
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_task():
    response = client.post("/api/tasks", json={"title": "Docker laboratory"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Docker laboratory"
    assert data["completed"] is False

def test_empty_task_is_rejected():
    response = client.post("/api/tasks", json={"title": "   "})
    assert response.status_code == 400
