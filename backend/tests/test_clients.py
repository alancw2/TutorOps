def test_create_client_success(client):
    res = client.post("/clients/", json={
        "first_name": "Alan",
        "last_name": "Ward",
        "email": "alan@example.com",
        "phone": None,
        "subject": "Math",
        "hourly_rate": 40.0
    })
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == 1
    assert data["email"] == "alan@example.com"
    assert data["hourly_rate"] == 40.0


def test_get_client_404(client):
    res = client.get("/clients/999")
    assert res.status_code == 404


def test_list_clients(client):
    client.post("/clients/", json={
        "first_name": "A",
        "last_name": "B",
        "email": "a@b.com",
        "phone": None,
        "subject": None,
        "hourly_rate": 30.0
    })
    res = client.get("/clients/")
    assert res.status_code == 200
    assert len(res.json()) == 1