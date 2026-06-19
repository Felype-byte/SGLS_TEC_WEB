import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page_is_running(client):
    """Testa se a página de login está retornando status 200 (OK)"""
    response = client.get('/login')
    assert response.status_code == 200

def test_app_is_running(client):
    """Testa se a página inicial redireciona usuários não autenticados (status 302)"""
    response = client.get('/')
    assert response.status_code == 302