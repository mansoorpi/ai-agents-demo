from fastapi.testclient import TestClient
import api

client = TestClient(api.app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_upload_rejects_unsupported():
    response = client.post('/documents', files={'file': ('x.exe', b'bad', 'application/octet-stream')})
    assert response.status_code == 400
