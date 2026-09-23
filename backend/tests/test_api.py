import os

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.main import Base, app, engine


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as client:
        yield client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task(client):
    response = client.post(
        "/api/tasks",
        json={"title": "Docker laboratory"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Docker laboratory"
    assert data["completed"] is False


def test_empty_task_is_rejected(client):
    response = client.post(
        "/api/tasks",
        json={"title": "   "},
    )

    assert response.status_code == 400