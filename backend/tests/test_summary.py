def _create_client(client, email, hourly_rate):
    res = client.post("/clients/", json={
        "first_name": "X",
        "last_name": "Y",
        "email": email,
        "phone": None,
        "subject": None,
        "hourly_rate": hourly_rate
    })
    return res.json()["id"]


def _create_session(client, client_id, hours):
    return client.post("/sessions/", json={
        "client_id": client_id,
        "date": "2026-02-21",
        "duration_hours": hours,
        "topic": None,
        "notes": None
    })


def test_client_summary_math(client):
    cid = _create_client(client, "c1@example.com", 50.0)
    _create_session(client, cid, 1.0)
    _create_session(client, cid, 2.5)

    res = client.get(f"/clients/{cid}/summary")
    assert res.status_code == 200
    data = res.json()

    assert data["client_id"] == cid
    assert data["total_sessions"] == 2
    assert abs(data["total_hours"] - 3.5) < 1e-9
    assert abs(data["total_earnings"] - 175.0) < 1e-9  # 3.5 * 50


def test_global_summary_math(client):
    c1 = _create_client(client, "c1@example.com", 40.0)
    c2 = _create_client(client, "c2@example.com", 60.0)

    _create_session(client, c1, 2.0)  # 80
    _create_session(client, c2, 1.0)  # 60
    _create_session(client, c2, 0.5)  # 30

    res = client.get("/summary")
    assert res.status_code == 200
    data = res.json()

    assert data["total_clients"] == 2
    assert data["total_sessions"] == 3
    assert abs(data["total_hours"] - 3.5) < 1e-9
    assert abs(data["total_earnings"] - 170.0) < 1e-9  # 80+60+30