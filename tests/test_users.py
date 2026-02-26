import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    response = await client.post(
        "/users/",
        json={"email": "alice@example.com", "full_name": "Alice Smith"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["full_name"] == "Alice Smith"
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient) -> None:
    payload = {"email": "bob@example.com", "full_name": "Bob Jones"}
    await client.post("/users/", json=payload)
    response = await client.post("/users/", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient) -> None:
    create_resp = await client.post(
        "/users/",
        json={"email": "carol@example.com", "full_name": "Carol White"},
    )
    user_id = create_resp.json()["id"]

    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "carol@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient) -> None:
    response = await client.get("/users/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_users_pagination(client: AsyncClient) -> None:
    for i in range(5):
        await client.post(
            "/users/",
            json={"email": f"user{i}@example.com", "full_name": f"User {i}"},
        )

    response = await client.get("/users/?skip=0&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    assert data["total"] == 5
    assert data["skip"] == 0
    assert data["limit"] == 3


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient) -> None:
    create_resp = await client.post(
        "/users/",
        json={"email": "dave@example.com", "full_name": "Dave Brown"},
    )
    user_id = create_resp.json()["id"]

    response = await client.patch(f"/users/{user_id}", json={"full_name": "David Brown"})
    assert response.status_code == 200
    assert response.json()["full_name"] == "David Brown"
    assert response.json()["email"] == "dave@example.com"


@pytest.mark.asyncio
async def test_update_user_not_found(client: AsyncClient) -> None:
    response = await client.patch("/users/nonexistent-id", json={"full_name": "X"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient) -> None:
    create_resp = await client.post(
        "/users/",
        json={"email": "eve@example.com", "full_name": "Eve Green"},
    )
    user_id = create_resp.json()["id"]

    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    get_response = await client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_not_found(client: AsyncClient) -> None:
    response = await client.delete("/users/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    response = await client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
