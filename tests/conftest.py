from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import model




SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture
def test_user2(client):
    user_data = {"username": "example2", "email": "example2@example.com",
                 "password": "123456"}
    res= client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user =res.json()
    new_user['password'] = user_data["password"]
    return new_user
@pytest.fixture
def test_user(client):
    user_data = {"username": "example1", "email": "example@example.com",
                 "password": "123456"}
    res= client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user =res.json()
    new_user['password'] = user_data["password"]
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user['id']})
@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
 
@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [
        {
            "title": "First Title",
            "content": "First Content",
            "user_id": test_user['id']
            },
        {
            "title": "Second Title",
            "content": "Second Content",
            "user_id": test_user['id']
            },
        {
            "title": "Third Title",
            "content": "Third Content",
            "user_id": test_user['id']},
        {
            "title": "Fourth Title",
            "content": "Fourth Content",
            "user_id": test_user2['id']},
    ]
    def create_post_model(post):
        return model.Post(**post)
    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    session.add_all(posts)
    
    session.commit()
    session.query(model.Post).all()
    return posts