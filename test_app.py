# Place this file alongside app.py at the repo root.
# Requires DB_HOST/DB_NAME/DB_USER/DB_PASSWORD/DB_PORT/SECRET_KEY to already be
# set in the environment (the CI workflow sets these to point at the Postgres
# service container with a throwaway test SECRET_KEY).

import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_home_increments_counter(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"visited" in response.data


def test_register_and_login(client):
    response = client.post(
        "/register",
        data={"username": "testuser", "password": "testpass123"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    response = client.post(
        "/login",
        data={"username": "testuser", "password": "testpass123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Logged in as" in response.data


def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=True)
    # Not logged in — should be redirected to the login form
    assert b"Log in" in response.data
