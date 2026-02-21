def _create_client(client, hourly_rate=40.0):
    res = client.post("/clients/", json={
        "first_name": "Alan",
        "last_name": "Ward",
        "email": "alan@example.com",
        "phone": None,
        "subject": None,
        "hourly_rate": hourly_rate
    })
    return res.json()["id"]


def test_create_session_success(client):
    cid = _create_client(client)
    res = client.post("/sessions/", json={
        "client_id": cid,
        "date": "2026-02-21",
        "duration_hours": 1.5,
        "topic": "ODEs",
        "notes": None
    })
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == 1
    assert data["client_id"] == cid
    assert data["duration_hours"] == 1.5


def test_create_session_bad_client_404(client):
    res = client.post("/sessions/", json={
        "client_id": 999,
        "date": "2026-02-21",
        "duration_hours": 1.0,
        "topic": None,
        "notes": None
    })
    assert res.status_code == 404


def test_get_session_404(client):
    res = client.get("/sessions/999")
    assert res.status_code == 404