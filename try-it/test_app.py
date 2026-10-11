
import pytest
from app import app


# Fixture: setup and teardown
@pytest.fixture
def client():
    # Setup
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    # Teardown: runs after the test
    print("\nTeardown: Test client closed")


# Test 1: Home page
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Book" in response.data


# Test 2: Page returns HTML
def test_home_content_type(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.content_type


# Test 3: Cart page
def test_cart(client):
    response = client.get("/cart")

    assert response.status_code == 200


# Test 4: Invalid URL
def test_invalid_page(client):
    response = client.get("/this-page-does-not-exist")

    assert response.status_code == 404
