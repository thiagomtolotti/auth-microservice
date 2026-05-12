from .utils import settings


def test_settings():
    assert settings is not None
    assert settings.private_key is not None
    assert settings.public_key is not None

    assert "BEGIN PRIVATE KEY" in settings.private_key
    assert "BEGIN PUBLIC KEY" in settings.public_key
