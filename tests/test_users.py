from jose import jwt

from app import schemas
import pytest
from app.settings import JWT_SECRET, JWT_ALGORITHM

 
# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("message"))
    
#     assert res.json().get("message") == "API Service is up and running!"
#     assert res.status_code == 200
    
def test_create_user(client):
    res = client.post("/users", json={
        "email": "user@gmail.com",
        "password": "password123",
    })
    print(res.json())
    new_user = schemas.User(**res.json())
    
    assert new_user.email == "user@gmail.com"
    assert res.status_code == 201
    
def test_login_user(test_user, client):
    res = client.post("/auth/login", data={
        "username": test_user['email'],
        "password": test_user['password']
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    id = int(payload.get("sub"))
    
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
    
@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 403),
    ("user@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    (None, "password123", 403),
    ("user@gmail.com", None, 403),
])   
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/auth/login", data={
        "username": email,
        "password": password
    })
    
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid email or password"