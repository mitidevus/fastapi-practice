from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.settings import SQLALCHEMY_DATABASE_URL_TEST
from app.database import get_db_context, Base


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