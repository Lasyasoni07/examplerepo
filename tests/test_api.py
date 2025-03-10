import requests

BASE_URL = "http://127.0.0.1:5000"

# Test GET all users
def test_get_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test GET single user
def test_get_single_user():
    response = requests.get(f"{BASE_URL}/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"

# Test POST - Create a user
def test_create_user():
    payload = {"name": "Charlie", "email": "charlie@example.com"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Charlie"

# Test PUT - Update a user
def test_update_user():
    payload = {"name": "Updated Alice"}
    response = requests.put(f"{BASE_URL}/users/1", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Alice"

# Test DELETE a user
def test_delete_user():
    response = requests.delete(f"{BASE_URL}/users/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"
