
def test_index_route(client):

    response = client.get("/")
    html = response.data.decode()
    assert response.status_code == 200
    assert '<label for="basic-url" class="form-label">Бесплатно проверяйте сайты на SEO-пригодность</label>' in html

def test_get_url_route(client):

    response = client.get("/url/1000000000")
    assert response.status_code == 404
    

def test_get_urls_route(client):

    response = client.get("/urls")
    html = response.data.decode()
    assert response.status_code == 200
    assert '<table class="table table-bordered table-hover text-nowrap" data-test="urls">' in html

def test_post_check_route(client):

    response = client.post("/urls/10000000000/checks")
    assert response.status_code == 404