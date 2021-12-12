from fastapi import status
from httpx import AsyncClient


async def test_user_me(client: AsyncClient, user_token_headers):
    res = await client.get("/users/me", headers=user_token_headers)
    assert res.status_code == status.HTTP_200_OK


async def test_user_without_login(client: AsyncClient):
    res = await client.get(
        "/users/me",
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
