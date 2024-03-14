import pytest
from jose import jwt
from app import schema
from app.config import settings

def test_create_user(client):
    res = client.post("/users", json={"username": "jeremiah4", "email": "user4@example.com", "password": "password"})
    new_user = schema.UserOut(**res.json())
    assert new_user.username == "jeremiah4"
    assert res.status_code == 201

def test_login_user( test_user,client):
    res = client.post("/login", data={"username": test_user['username'], "password": test_user['password']})
    login_res = schema.Token(**res.json())
    payload= jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("username, password, status_code", [
    ('jeremiad1', 'password123', 403),
    ('jeremiah1213', 'wrongPassword', 403),
    ('jeremiah21', 'wrongPassword', 403),
    (None, 'password123', 422),
    ('jeremiah1231', None, 422)
])
def test_incorrect_login(client, username, password, status_code):
    res = client.post("/login", data={"username": username, "password": password})
    assert res.status_code == status_code