import requests

BASE_URL = "http://127.0.0.1:5000"

#  1. Get all users
def get_users():
    response = requests.get(f"{BASE_URL}/users")
    print(response.status_code, response.json())

#  2. Create a new user (POST)
def create_user():
    payload = {"name": "rosestella", "email": "rosestella@example.com"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    print(response.status_code, response.json())

#  3. Get a single user by ID
def get_user(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(response.status_code, response.json())

#  4. Update a user (PUT)
def update_user(user_id):
    payload = {"name": "Alice", "email": "alice@example.com"}
    response = requests.put(f"{BASE_URL}/users/{1}", json=payload)
    print(response.status_code, response.json())

#  5. Delete a user (DELETE)
def delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/users/{3}")
    print(response.status_code, response.json())

#  Run API calls one by one
if __name__ == "__main__":
    get_users()        # Fetch all users
    create_user()      # Create a new user
    get_user(3)        # Fetch the new user (ID = 3)
    update_user(3)     # Update user details
    delete_user(3)     # Delete user
