import pytest
import json
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_welcome(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'usage' in data

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_valid_user(client):
    response = client.get('/octocat')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'username' in data
    assert 'gists' in data
    assert 'count' in data
    assert 'status' in data
    assert data['status'] == 'success'

def test_invalid_user(client):
    response = client.get('/user_not_exist_xyz_12345')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['status'] == 'error'

def test_username_in_response(client):
    response = client.get('/octocat')
    data = json.loads(response.data)
    assert data['username'] == 'octocat'
