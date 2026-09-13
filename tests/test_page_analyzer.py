import pytest

from page_analyzer.app import app


@pytest.fixture()
def client():

    app.config['TESTING'] = True
    client = app.test_client()

    yield client
    

def test_index_route(client):

    response = client.get("/")
    html = response.data.decode()
    assert response.status_code == 200
    assert 'Бесплатно проверяйте сайты на SEO-пригодность' in html


def test_get_url_route(client):

    response = client.get("/url/1000000000")
    assert response.status_code == 404