import pytest
from app import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        init_db()
        yield client

def test_home(client):
    res = client.get('/')
    assert res.status_code == 200

def test_add_task(client):
    res = client.post('/add', data={'title': 'Test task'})
    assert res.status_code == 302