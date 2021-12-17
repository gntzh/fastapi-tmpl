import pytest
from fastapi import status
from httpx import AsyncClient

from src.domain import User

pytestmark = pytest.mark.anyio


async def test_create_item(
    client: AsyncClient, user_token_headers, test_user: User
) -> None:
    data = {"title": "Foo", "description": "nothing"}
    res = await client.post(
        "/items/",
        headers=user_token_headers,
        json=data,
    )
    assert res.status_code == status.HTTP_201_CREATED
    j = res.json()
    assert j["title"] == data["title"]
    assert j["description"] == data["description"]
    assert "id" in j
    assert j["owner_id"] == str(test_user.id)


async def test_read_item(
    client: AsyncClient, user_token_headers, test_user: User
) -> None:
    data = {"title": "Foo", "description": "nothing"}
    res = await client.post(
        "/items/",
        headers=user_token_headers,
        json=data,
    )
    assert res.status_code == 201
    j = res.json()
    assert j["title"] == data["title"]
    assert j["description"] == data["description"]
    assert "id" in j
    assert j["owner_id"] == str(test_user.id)
