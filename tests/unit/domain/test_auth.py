from src.domain.user import User


def test_register():
    user = User.register(
        username="test", email="email@example.com", password="testpassword"
    )
    assert not user.is_superuser
    assert not user.email_verified


def test_create_superuser():
    user = User.create_superuser(
        username="test", email="email@example.com", password="testpassword"
    )
    assert user.is_superuser
    assert not user.email_verified
