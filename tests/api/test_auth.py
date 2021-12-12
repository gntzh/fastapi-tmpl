import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_success_register(client: AsyncClient, email_outbox):
    data = {
        "username": "test_register_user",
        "email": "test_register_user@example.com",
        "password": "passoword",
    }
    email_num = len(email_outbox)
    res = await client.post("/auth/register/", json=data)
    assert email_num + 1 == len(email_outbox)
    j = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert j["username"] == data["username"]


@pytest.mark.parametrize(
    "username, email",
    (
        ("test_user", None),
        (None, "test_user@example.com"),
    ),
)
async def test_register_with_existed(
    username, email, client: AsyncClient, email_outbox, test_user
):
    data = {
        "username": username or "test_register_with_existed",
        "email": email or "test_register_with_existed@example.com",
        "password": "passoword",
    }
    res = await client.post("/auth/register/", json=data)
    print(res.text)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


async def test_get_token(client: AsyncClient, test_user):
    res = await client.post(
        "/auth/token/",
        data={
            "username": "test_user",
            "password": "test_user",
            "grant_type": "password",
        },
    )
    j = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert "access_token" in j
    assert "refresh_token" in j


@pytest.mark.parametrize(
    "username, password",
    (("test_user", "wrong"), ("wrong", "test_user")),
)
async def test_get_token_when_wrong_username_or_password(
    client: AsyncClient,
    username,
    password,
):
    res = await client.post(
        "/auth/token/", data={"username": username, "password": password}
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST
