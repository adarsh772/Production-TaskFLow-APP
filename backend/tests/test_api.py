def _register_and_login(client, username="alice"):
    client.post(
        "/user/register",
        json={
            "name": "Alice",
            "username": username,
            "email": f"{username}@example.com",
            "password": "supersecret123",
        },
    )
    resp = client.post(
        "/user/login",
        json={"username": username, "password": "supersecret123"},
    )
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_health_check(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_register_and_login(client):
    resp = client.post(
        "/user/register",
        json={
            "name": "Bob",
            "username": "bob",
            "email": "bob@example.com",
            "password": "supersecret123",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["username"] == "bob"

    resp = client.post(
        "/user/login", json={"username": "bob", "password": "supersecret123"}
    )
    assert resp.status_code == 200
    assert "token" in resp.json()


def test_login_wrong_password(client):
    client.post(
        "/user/register",
        json={
            "name": "Carl",
            "username": "carl",
            "email": "carl@example.com",
            "password": "supersecret123",
        },
    )
    resp = client.post(
        "/user/login", json={"username": "carl", "password": "wrongpass"}
    )
    assert resp.status_code == 401


def test_task_requires_auth(client):
    resp = client.get("/tasks/all_task")
    assert resp.status_code == 401


def test_task_crud_flow(client):
    headers = _register_and_login(client, "dana")

    resp = client.post(
        "/tasks/create",
        json={"title": "Write tests", "description": "Cover the API", "is_completed": False},
        headers=headers,
    )
    assert resp.status_code == 201
    task_id = resp.json()["data"]["id"]

    resp = client.get("/tasks/all_task", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()["tasks"]) == 1

    resp = client.put(
        f"/tasks/update/{task_id}",
        json={"title": "Write tests", "description": "Cover the API", "is_completed": True},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["is_completed"] is True

    resp = client.delete(f"/tasks/delete/{task_id}", headers=headers)
    assert resp.status_code == 204

    resp = client.get(f"/tasks/getby_id/{task_id}", headers=headers)
    assert resp.status_code == 404


def test_tasks_are_scoped_per_user(client):
    headers_a = _register_and_login(client, "erin")
    headers_b = _register_and_login(client, "frank")

    resp = client.post(
        "/tasks/create",
        json={"title": "Erin's task", "description": "private", "is_completed": False},
        headers=headers_a,
    )
    task_id = resp.json()["data"]["id"]

    # Frank should not be able to see or modify Erin's task.
    resp = client.get(f"/tasks/getby_id/{task_id}", headers=headers_b)
    assert resp.status_code == 404

    resp = client.get("/tasks/all_task", headers=headers_b)
    assert resp.json()["tasks"] == []
