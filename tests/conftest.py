from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.settings import SQLALCHEMY_DATABASE_URL_TEST
from app.database import get_db_context, Base
from app.services.auth import create_access_token
from app import models

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db_context():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db_context] = override_get_db_context
    yield TestClient(app)
    
@pytest.fixture
def test_user(client):
    user_data = {
        "email": "user@gmail.com",
        "password": "password123",
    }
    res = client.post("/users", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "user2@gmail.com",
        "password": "password123",
    }
    res = client.post("/users", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "Post 1",
            "content": "Content of post 1",
            "owner_id": test_user['id']
        },
        {
            "title": "Post 2",
            "content": "Content of post 2",
            "owner_id": test_user['id']
        },
        {
            "title": "Post 3",
            "content": "Content of post 3",
            "owner_id": test_user['id']
        },
        {
            "title": "Post 4",
            "content": "Content of post 4",
            "owner_id": test_user2['id']
        }
    ]
    
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts_lists = list(post_map)
    
    session.add_all(posts_lists)
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts