from fastapi import status
from httpx import AsyncClient

from src.domain.user import User


async def test_user_me(client: AsyncClient, user_token_headers):
    res = await client.get("/users/me/", headers=user_token_headers)
    assert res.status_code == status.HTTP_200_OK


async def test_user_without_login(client: AsyncClient):
    res = await client.get(
        "/users/me/",
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


async def test_update_profile(client: AsyncClient, user_token_headers):
    data = {"email": "update_profile@example.com"}
    res = await client.patch("/users/me/", headers=user_token_headers, json=data)
    assert res.status_code == status.HTTP_200_OK
    j = res.json()
    assert j["email"] == data["email"]
    assert not j["email_verified"]

    data = {"email": "test_user@example.com"}
    res = await client.patch("/users/me/", headers=user_token_headers, json=data)
    assert res.status_code == status.HTTP_200_OK
    j = res.json()
    assert j["email"] == data["email"]
    assert not j["email_verified"]


async def test_list_users(client: AsyncClient, superuser_token_headers):
    res = await client.get("/users/", headers=superuser_token_headers)
    assert res.status_code == status.HTTP_200_OK
    j = res.json()
    assert isinstance(j["total_count"], int)
    assert isinstance(j["items"], list)


async def test_get_user(client: AsyncClient, superuser_token_headers, test_user: User):
    res = await client.get(f"/users/{test_user.id}/", headers=superuser_token_headers)
    assert res.status_code == status.HTTP_200_OK
    j = res.json()
    assert j["username"] == test_user.username
    assert j["email"] == test_user.email


async def test_create_and_delete_user(client: AsyncClient, superuser_token_headers):
    data = {
        "username": "create_delete",
        "password": "create_delete",
        "email": "create_delete@example.com",
    }
    res = await client.post("/users/", headers=superuser_token_headers, json=data)

    assert res.status_code == status.HTTP_200_OK
    j = res.json()
    assert "id" in j
    assert j["username"] == data["username"]
    assert j["email"] == data["email"]

    res = await client.delete(f"/users/{j['id']}/", headers=superuser_token_headers)
    assert res.status_code == status.HTTP_204_NO_CONTENT
