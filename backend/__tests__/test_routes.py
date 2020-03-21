import pytest
import json
import fakeredis
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    yield app.test_client()

@pytest.fixture
def redis_server():
    server = fakeredis.FakeServer()
    yield(server)

def test_hello_world(client):
    hw = client.get('/')
    resp = json.loads(hw.data)
    hw_response = { 'hello': 'world' }
    assert hw.status_code == 200
    assert resp == hw_response, hw

def test_post_data(client, redis_server):
    post_usn_pw = client.post('/scrape_data')
    resp = json.loads(post_usn_pw.data)
    response = {}
    assert resp.status_code == 200
    assert resp